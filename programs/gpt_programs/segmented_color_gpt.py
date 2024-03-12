import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define the two colors
color1 = [0, 0, 1]  # Blue color
color2 = [1, 0, 0]  # Red color

# Define the positions of the colors in the colormap
positions = [0.0, 1.0]

# Create a list of colors and their positions
colors = [color1, color2]

# Create a colormap using LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_colormap', list(zip(positions, colors)))

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plotting with the custom colormap
plt.scatter(x, y, c=y, cmap=cmap)
plt.colorbar(label='Value')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Custom Colormap from Blue to Red')
plt.show()
