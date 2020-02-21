"""
NCL_vector_4.py
========
Concepts illustrated:
  - Coloring vectors based on temperature data
  - Changing the scale of the vectors on the plot

Plot U & V vectors globally, colored according to temperature

This Python script reproduces the NCL plot script found here:  https://www.ncl.ucar.edu/Applications/Scripts/vector_4.ncl

The NCL graphics and description for this script are found here: https://www.ncl.ucar.edu/Applications/vector.shtml#ex4
"""

###############################################################################
# Import necessary packages
import xarray as xr
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs
from geocat.viz import cmaps
from geocat.viz.util import add_lat_lon_ticklabels, nclize_axis, truncate_colormap

###############################################################################
# Read in data from netCDF file.
# Note that when we extract ``U``, ``V``, and ``T``,
# we only read a subset of latitude and longitude.
# This choice was made because ``geocat.viz`` doesn’t offer
# an equivalent function to ncl’s ``vcMinDistanceF`` yet.

file_in = xr.open_dataset('../../data/netcdf_files/83.nc')
# Our dataset is a subset of the data from the file
ds = file_in.isel(time=0, lev=12, lon=slice(0,-1,5), lat=slice(2,-1,3))

###############################################################################
# Make the plot.
# Because there is no equivalent to ``CurlyVector`` in ``geocat.viz``,
# this plot does not look as good as the NCL version.

# Set up figure and axes
fig, ax = plt.subplots(figsize=(10, 6.25))
ax = plt.axes(projection=ccrs.PlateCarree())
fig.suptitle('Vectors colored by a scalar map', fontsize=14, y=.9)
nclize_axis(ax)
add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xticks(range(-180, 181, 30))
plt.yticks(range(-90, 91, 30))

# Draw vector plot
# (there is no matplotlib equivalent to "CurlyVector" yet)
plt.cm.register_cmap('BlAqGrYeOrReVi200', truncate_colormap(cmaps.BlAqGrYeOrReVi200, minval=0.03, maxval=0.95, n=16))
cmap = plt.cm.get_cmap('BlAqGrYeOrReVi200', 16)
Q = plt.quiver(ds['lon'], ds['lat'], ds['U'].data, ds['V'].data, ds['T'].data, cmap=cmap,
               zorder=1, pivot="middle", width=0.001)
plt.clim(228, 292)

# Draw legend for vector plot
ax.add_patch(plt.Rectangle((150, -140), 30, 30, facecolor='white', edgecolor='black', clip_on=False))
qk = ax.quiverkey(Q, 0.87, 0.05, 10, r'10 $m/s$', labelpos='N',
                  coordinates='figure', color='black')
ax.set_title('Temperature', y=1.04, loc='left')
ax.set_title('$^{\circ}$K', y=1.04, loc='right')

cax = plt.axes((0.225, 0.075, 0.55, 0.025))
cbar = fig.colorbar(Q, ax=ax, cax=cax, orientation='horizontal',
                    ticks=range(232,289,8), drawedges=True)

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=0)

# Generate plot!
plt.show()
