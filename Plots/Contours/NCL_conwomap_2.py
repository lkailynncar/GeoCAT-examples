"""
NCL_conwomap_2.py
===============
Concepts illustrated:
   - Drawing a simple filled contour plot
   - Selecting a different color map
   - Changing the size/shape of a contour plot using viewport resources

This Python script reproduces the NCL plot script found here: https://www.ncl.ucar.edu/Applications/Scripts/conwomap_2.ncl

The NCL graphics and description for this script are found here: https://www.ncl.ucar.edu/Applications/conwomap.shtml#ex2
"""

###############################################################################
# Import packages
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from geocat.viz.util import make_byr_cmap

import matplotlib.pyplot as plt
import matplotlib.ticker as tic

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset("../../data/netcdf_files/cone.nc")
u = ds.u.isel(time=4)

###############################################################################
# Plot

# First get axes for a projection of preference
fig = plt.figure()
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Adjust figure size and plot parameters to get identical to original NCL plot
fig.set_size_inches((10, 6))

# Hard-code tic values. This assumes data are global
ax.set_xticks(np.linspace(0, 40, 5))
ax.set_yticks(np.linspace(0, 25, 6))

# Adjust axes limits
ax.set_xlim((0,49))
ax.set_ylim((0,29))

# Set axes labels
ax.set_xlabel("X", fontsize=18, y=1.04)
ax.set_ylabel("Y", fontsize=18)


# Tweak minor tic marks. Set spacing so we get nice round values (10 degrees). Again, assumes global data
ax.tick_params(labelsize=16)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
ax.tick_params('both', length=12, width=0.5, which='major', top=True, right=True)
ax.tick_params('both', length=8, width=0.5, which='minor', top=True, right=True)

# Add titles to left and right of the plot axis.
ax.set_title('Cone amplitude', y=1.04, fontsize=18, loc='left')
ax.set_title('ndim', y=1.04, fontsize=18, loc='right')

# Import an NCL colormap
newcmp = make_byr_cmap()

# Plot filled contours
p = u.plot.contourf(ax=ax, vmin=-1, vmax=10, levels=12, cmap=newcmp, add_colorbar=False, transform=projection, extend='neither', add_labels=False)
# Plot borderlines first
u.plot.contour(ax=ax, vmin=-1, vmax=10, levels=12, linewidths=0.5, colors='k', add_colorbar=False, transform=projection, extend='neither', add_labels=False)

# Add horizontal colorbar
cbar = plt.colorbar(p, orientation='horizontal', shrink=0.5)
cbar.ax.tick_params(labelsize=16)
cbar.set_ticks(np.linspace(0, 9, 10))

# Show the plot
plt.show()
