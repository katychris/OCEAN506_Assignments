import numpy as np
from scipy.io import loadmat
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib import path
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
import seaborn as sns

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        mticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
             self.format = r'$\mathdefault{%s}$' % self.format

# # Load in the data
# path = '/Users/kchristensen/Desktop/Data/Vertical_Velocity/W_errs_global_20200211.mat'
# data = loadmat(path,squeeze_me=True)
# W = data['W'];W_var = data['W_variance']
# lat = data['LAT'];lon = data['LON']
# flt = data['FloatNum'];cyc = data['CycNum']

path = '/Users/kchristensen/Desktop/Werrs_global_021120.mat'
data = loadmat(path,squeeze_me=True)
W = data['DT'];W_var = data['DT_v']
lat = data['LAT'];lon = data['LON']

# Set the parameters to select out just a portion of the data
lon_min = -160;lon_dx = 20
lat_min = -60; lat_dy = 15
fs = 15
clr = '#4e574e'
plt.rcParams.update({'font.size': fs})
plt.close('all')

# Select out the data within the designated square
mask = (lon>=lon_min) & (lon<=lon_min+lon_dx) & (lat>=lat_min) & (lat<=lat_min+lat_dy)

# Subplot #1: Map
# ---------------------------------------------------------------------------------------
# Create a map to geolocate our specific area on the world
fig = plt.figure()
ax1 = fig.add_subplot(221,projection=ccrs.Mollweide(central_longitude=lon_min+lon_dx/2))
ax1.set_global()
ax1.add_patch(mpatches.Rectangle(xy=[lon_min, lat_min], width=lon_dx, height=lat_dy,
                                    facecolor=clr,edgecolor='k',
                                    transform=ccrs.PlateCarree()))
ax1.coastlines(color='#737373')
plt.title('a.',loc='left')

# Subplot #2: Zoomed-in Map 
# ---------------------------------------------------------------------------------------
# Create a plot with the same outside color as shown on the larger map
ax2 = fig.add_subplot(222,projection=ccrs.PlateCarree())
ax2.outline_patch.set_linewidth(3)
ax2.background_patch.set_facecolor(clr)
ax2.set_xlim([lon_min-1,lon_min+lon_dx+1])
ax2.set_ylim([lat_min-1,lat_min+lat_dy+1])

# Create the scatter with all of the data from our selected area
# Also create/format a colorbar to go with: note that this is a log scale colorbar
sc = plt.scatter(lon[mask],lat[mask],20,W[mask],cmap='RdBu',vmin=-np.nanmax(W[mask]),
	norm=colors.SymLogNorm(linthresh=5e-4,vmin=-np.nanmax(W[mask]), vmax=np.nanmax(W[mask])))
c = plt.colorbar(sc,format=OOMFormatter(-3, mathText=False),extend='both',
	label='Vertical Velocity | w (m/s)',
    ticks=[-8e-3,-4e-3,-2e-3,-1e-3,-5e-4,0,5e-4,1e-3,2e-3,4e-3,8e-3])

# Format the grid lines and axis labels
gl = ax2.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                 color='gray', alpha=0.5, linestyle='-')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlocator = mticker.FixedLocator(np.arange(lon_min-10,lon_min+lon_dx+10,5))
gl.ylocator = mticker.FixedLocator(np.arange(lat_min-4,lat_min+lat_dy+4,2))
gl.xlabel_style = {'color': 'gray'}
gl.ylabel_style = {'color': 'gray'}
plt.title('b.',loc='left')

# Subplot #3: Histogram
# ---------------------------------------------------------------------------------------
# Create the subplot turn off the right and top axes
ax3 = fig.add_subplot(212)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)

# Plot the histogram and the kde
sns.distplot(W[mask],bins=100,
	hist_kws={"color": clr,"alpha":0.9,"ec":'k'},
	kde_kws={"color": "k", "lw": 3, "label": "KDE"})
ax3.set_xlabel('Vertical Velocity | w (m/s)')
ax3.set_ylabel('Density Function')
plt.title('c.',loc='left')

plt.show()
