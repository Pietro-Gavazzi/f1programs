import fastf1 as ff1
from  fastf1.plotting import driver_color, team_color,  DRIVER_TRANSLATE



import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
import matplotlib.colors as mcolors


from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d







def get_driver_lap_telemetry(lap):

    # Index(['Date', 'SessionTime', 'DriverAhead', 'DistanceToDriverAhead', 'Time',
    #    'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS', 'Source',
    #    'Distance', 'RelativeDistance', 'Status', 'X', 'Y', 'Z'],

    distance= lap.telemetry['Distance'].copy()   # get distance as x-value for spline

    # Get telemetry data
    x = lap.telemetry['X'].copy()              # values for x-axis in m
    spline_x = interp1d(distance, x, kind='linear')

    y = lap.telemetry['Y'].copy()               # values for y-axis in m
    spline_y = interp1d(distance, y, kind='linear')

    z = lap.telemetry['Z'].copy()               # values for z-axis in m
    spline_z = interp1d(distance, z, kind='linear')


    speed = lap.telemetry['Speed'].copy() /3.6      # speed in m/s 
    spline_speed = interp1d(distance, speed, kind='linear')


    throttle = lap.telemetry['Throttle'].copy()     # 
    spline_throttle = interp1d(distance, throttle, kind='linear')    

    time = lap.telemetry['Time'].copy()           #time in s
    time = [float(i.to_timedelta64())*10**(-9) for i in time]
    spline_time = interp1d(distance, time, kind='linear')

    drs = [i in  [10, 12, 14] for i in lap.telemetry["DRS"]]
    spline_drs = interp1d(distance, drs, kind='linear')

    gear = lap.telemetry["nGear"]
    spline_gear = interp1d(distance, gear, kind='linear')


    max_distance = max(distance)
    min_distance = min(distance)
    
    return spline_x, spline_y, spline_z, spline_speed, spline_time, spline_drs, spline_gear, spline_throttle, (min_distance, max_distance), float(lap.LapTime.to_timedelta64())*10**(-9)






def cosine_similarity(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity


def print_circuit( x, y, value,  session,  pil_neg, pil_pos, limits_coordinates, nb_col, scale_name):


    weekend = session.event


    name_pil_pos = DRIVER_TRANSLATE[pil_pos]
    name_pil_neg = DRIVER_TRANSLATE[pil_neg]

    ##############################################################################
    # Now, we create a set of line segments so that we can color them
    # individually. This creates the points as a N x 1 x 2 array so that we can
    # stack points  together easily to get the segments. The segments array for
    # line collection needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)


    ##############################################################################
    # After this, we can actually plot the data.

    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(f'{weekend.Country} {weekend.year} - {session.name} fastest lap - {name_pil_neg} vs {name_pil_pos}', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(x, y, color='black', linestyle='-', linewidth=16, zorder=0)



    # Create a continuous norm to map from data points to colors
    color_pil_pos = driver_color(pil_pos)
    color_pil_neg = driver_color(pil_neg)


    cpil_pos = mcolors.to_rgb(color_pil_pos)
    cpil_neg  = mcolors.to_rgb(color_pil_neg)


    if (cosine_similarity(cpil_neg, cpil_pos)>0.9):
        cpil_pos = (1,0,0)
        cpil_neg = (0,1,0)
    

    
    diff_pil_neg = value.min()
    diff_pil_pos = value.max()


    abs_diff_pil_neg = abs(diff_pil_neg)
    abs_diff_pil_pos = abs(diff_pil_pos)


    extremety = max(abs_diff_pil_neg, abs_diff_pil_pos)


    c11 = (abs_diff_pil_neg)/(extremety)
    c12 = (extremety-abs_diff_pil_neg)/(extremety)
    c21 = (extremety-abs_diff_pil_pos)/(extremety)
    c22 = (abs_diff_pil_pos)/(extremety)  

    # print (c11, c12, c21, c22)

    c1 = np.array(cpil_neg)*c11 + np.array((1,1,1))*c12
    c2 = np.array((1,1,1))*c21 + np.array(cpil_pos)*c22


    n = nb_col//(c11+c22)
    n1 = int(c11*n)
    n2 = int(c22*n)
    # print(n1, n2)


    color_values = list(np.linspace(c1, (1,1,1),n1))+list(np.linspace((1,1,1), c2, n2))
    colormap = ListedColormap(color_values)
    lc = LineCollection(segments, cmap=colormap, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(value)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.5, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=value.min(), vmax=value.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal", label=f" ← {pil_neg} faster | {scale_name} | {pil_pos} faster → ")



    # scatter the sectors limimits
    for (x_coord, y_coord)  in limits_coordinates:
        ax.scatter(x_coord, y_coord,  color='black', linewidths=20, marker='*')

    # scatter the starting line 
    ax.scatter((x[-1]+x[0])/2, (y[-1]+y[0])/2,  color='black', linewidths=30, marker='*')

    # Show the plot
    return fig, ax