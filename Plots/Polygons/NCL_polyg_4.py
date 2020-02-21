"""
NCL_polyg_4.py
==============
Concepts illustrated:
  - Drawing a cylindrical equidistant map
  - Zooming in on a particular area on a cylindrical equidistant map
  - Attaching an outlined box to a map plot
  - Attaching filled polygons to a map plot
  - Filling in polygons with a shaded pattern
  - Changing the color and thickness of polylines
  - Changing the color of a filled polygon
  - Labeling the lines in a polyline
  - Changing the density of a fill pattern
  - Adding text to a plot

This Python script reproduces the NCL plot script found here: https://www.ncl.ucar.edu/Applications/Scripts/polyg_4.ncl

The NCL graphics and description for this script are found here: https://www.ncl.ucar.edu/Applications/polyg.shtml#ex4
"""

###############################################################################
# Import the necessary python libraries
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.viz as gcv
from matplotlib.ticker import AutoMinorLocator


ds = xr.open_dataset("../../data/netcdf_files/uv300.nc").isel(time=1)


###############################################################################
# Define a function to create the basic contour plot, which will get used twice
# to create two slightly different plots.

def make_base_plot():

    # First add continents
    continents = cartopy.feature.NaturalEarthFeature(
        name="coastline",
        category="physical",
        scale="50m",
        edgecolor="None",
        facecolor="lightgray",
    )

    map_extent = [-130, 0, -20, 40]
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(continents)
    ax.set_extent(map_extent, crs=ccrs.PlateCarree())

    # Specify contour levels (from -12 to 40 by 4).   The top range value of 44 is not included in the levels.
    levels = np.arange(-12, 44, 4)

    # Using a dictionary prevents repeating the same keyword arguments twice for the contours.
    kwargs = dict(
        levels=levels,  # contour levels specified outside this function
        xticks=[-120, -90, -60, -30, 0],  # nice x ticks
        yticks=[-20, 0, 20, 40],  # nice y ticks
        transform=ccrs.PlateCarree(),  # ds projection
        add_colorbar=False,  # don't add individual colorbars for each plot call
        add_labels=False,  # turn off xarray's automatic Lat, lon labels
        colors="gray",  # note plurals in this and following kwargs
        linestyles="-",
        linewidths=0.5,
    )

    # Create contour plot
    hdl = ds.U.plot.contour(
        x="lon",  # not strictly necessary but good to be explicit
        y="lat",
        ax=ax,    # this is the axes object we want to plot to
        **kwargs,
    )

    # Add contour labels.   Default contour labels are sparsely placed, so we specify label locations manually.
    # Label locations only need to be approximate; the nearest contour will be selected.
    label_locations = [(-123, 35), (-116, 17), (-94, 4), (-85, -6), (-95, -10),
                       (-85, -15), (-70, 35), (-42, 28), (-54, 7), (-53, -5),
                       (-39, -11), (-28, 11), (-16, -1), (-8, -9),             # Python allows trailing list separators.
                       ]
    ax.clabel(hdl,
              np.arange(-8, 24, 8),    # Only label these contour levels: [-8, 0, 8, 16]
              fontsize="small",
              colors="black",
              fmt="%.0f",              # Turn off decimal points
              manual=label_locations,  # Manual label locations
              inline=False)            # Don't remove the contour line where labels are located.

    # Create a rectangle patch, to color the border of the rectangle a different color.
    # Specify the rectangle as a corner point with width and height, to help place border text more easily.
    left, width = -90, 45
    bottom, height = 0, 30
    right = left + width
    top = bottom + height

    p = plt.Rectangle((left, bottom), width, height, fill=False,
                      zorder=3,          # Plot on top of the purple box border.
                      edgecolor='red',
                      alpha=0.5)         # Lower color intensity.
    ax.add_patch(p)

    # Draw text labels around the box.
    # Change the default padding around a text box to zero, making it a "tight" box.
    # Create "text_args" to keep from repeating code when drawing text.
    text_shared_args = dict(
        fontsize=8,
        bbox=dict(boxstyle='square, pad=0', facecolor='white', edgecolor='white'),
    )

    # Draw top text
    ax.text(left + 0.6 * width, top, 'test',
            horizontalalignment='right',
            verticalalignment='center',
            **text_shared_args
            )

    # Draw bottom text.   Change text background to match the map.
    ax.text(left + 0.5 * width, bottom, 'test',
            horizontalalignment='right',
            verticalalignment='center',
            fontsize=8,
            bbox=dict(boxstyle='square, pad=0', facecolor='lightgrey', edgecolor='lightgrey'),
            )

    # Draw left text
    ax.text(left, top, 'test',
            horizontalalignment='center',
            verticalalignment='top',
            rotation=90,
            **text_shared_args
            )

    # Draw right text
    ax.text(right, bottom, 'test',
            horizontalalignment='center',
            verticalalignment='bottom',
            rotation=-90,
            **text_shared_args
            )

    # Add title and tick marks to match NCL conventions.
    ax.set_title('Zonal Wind', y=1.04, loc='left')
    ax.set_title('m/s', y=1.04, loc='right')

    # Add lower text box.  Box appears off-center, but this is to leave room
    # for lower-case letters that drop lower.
    ax.text(1.0, -0.20, "CONTOUR FROM -12 TO 40 BY 4",
            fontname='Helvetica',
            horizontalalignment='right',
            transform=ax.transAxes,
            bbox=dict(boxstyle='square, pad=0.15', facecolor='white', edgecolor='black'))

    gcv.util.nclize_axis(ax)
    gcv.util.add_lat_lon_ticklabels(ax)

    # Adjust minor tick spacing for the Y axis
    ax.yaxis.set_minor_locator(AutoMinorLocator(n=4))

    return ax


###############################################################################
# Create a figure showing text inside a box.

ax = make_base_plot()

# Draw text inside of box
ax.text(-60.0, 15.0, "sample",
        fontsize=11,
        horizontalalignment='center')

plt.show()


###############################################################################
# Define a helper function that draws a polygon and then erases its border
# with another polygon.

def draw_hatch_polygon(xvals, yvals, hatchcolor, hatchpattern):
    """ Draw a polygon filled with a hatch pattern, but with no edges on the polygon.
    """
    ax.fill(xvals, yvals,
            edgecolor=hatchcolor,
            zorder=-1,              # Place underneath contour map (larger zorder is closer to viewer).
            fill=False,
            linewidth=0.5,
            hatch=hatchpattern,
            alpha=0.3               # Reduce color intensity
            )

    # Hatch color and polygon edge color are tied together, so we have to draw a white polygon edge
    # on top of the original polygon to remove the edge.
    ax.fill(xvals, yvals,
            edgecolor='white',
            zorder=0,            # Place on top of other polygon (larger zorder is closer to viewer).
            fill=False,
            linewidth=1          # Slightly larger linewidth removes ghost edges.
            )


###############################################################################
# Create a second figure showing polygons with hatch patterns.

# Make this figure the thumbnail image on the HTML page.
# sphinx_gallery_thumbnail_number = 2

ax = make_base_plot()

x_points = [-90.0, -45.0, -45.0, -90.0, -90.0]
y_points = [ 30.0,  30.0,   0.0,   0.0,  30.0]

# Plot the hatch pattern "underneath" the red box, to hide the purple border that
# is unavoidably attached to producing the hatch pattern.

ax.fill(x_points, y_points,
        edgecolor='purple',   # Box hatch pattern is purple.
        zorder=2,             # Place on top of map (larger zorder is closer to viewer).
        fill=False,
        hatch='...',          # Adding more or fewer dots to '...' will change hatch density.
        linewidth=0.5,        # Make each dot smaller
        alpha=0.2             # Make hatch semi-transparent using alpha level in range [0, 1].
        )

# Now draw some triangles with various hatch pattern densities.

x_tri = np.array([-125, -115, -120])
y_tri = np.array([-15,   -10,    5])

draw_hatch_polygon(x_tri, y_tri, 'brown', '++++')

draw_hatch_polygon(x_tri + 10, y_tri, 'blue', '+++')

draw_hatch_polygon(x_tri + 20, y_tri, 'forestgreen', '++')

plt.show()
