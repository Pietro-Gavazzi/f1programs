from cProfile import label
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt

folder_name = "qualification_times/"
gp ="Bahrein"
pil1 = "LEC"
pil2 = "VER"

fig_name = folder_name+gp+"-qualif-"+pil1+"-"+pil2+".png"




ff1.Cache.enable_cache("C:/Users/pietr/Documents/trop_long/projet-f1")

plotting.setup_mpl()

session = ff1.get_session(2024, gp, 'Q')
session.load()


pilot1 = session.laps.pick_driver(pil1).pick_fastest()
pilot2 = session.laps.pick_driver(pil2).pick_fastest()

delta_time, ref_tel, compare_tel = utils.delta_time(pilot2, pilot1)
# ham is reference, lec is compared

fig, ax = plt.subplots()
# use telemetry returned by .delta_time for best accuracy,
# this ensure the same applied interpolation and resampling
ax.plot(ref_tel['Distance'], ref_tel['Speed'],
        color=plotting.driver_color(pil2), label=pil2+" speed")
ax.plot(compare_tel['Distance'], compare_tel['Speed'],
        color=plotting.driver_color(pil1), label=pil1+" speed")
ax.set_ylabel("speed (km/h)")
ax.set_xlabel("track distance (m)")
ax.legend()


twin = ax.twinx()
twin.plot(ref_tel['Distance'], delta_time, '--', color='white' )
twin.set_ylabel("<-- "+pil1+" ahead | "+pil2+" ahead -->")
twin.legend()


plt.savefig(fig_name)
plt.show()