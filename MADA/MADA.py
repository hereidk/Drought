'''
Created on Dec 17, 2012

@author: kahere
'''

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import cm

def Plotter(year):
        
        plt.figure(3)
        # Define basemap
        m = Basemap(projection='cyl',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=60,
                    urcrnrlon=lon.max(),lat_ts=30,resolution='l')
        
        # Set colormap
        my_cmap = cm.get_cmap('RdYlBu')
        
#         pdsi_index = {-4:'Extreme drought', -3:'Severe drought', -2:'Moderate drought',
#                       -1:'Slightly dry', 0:'Average', 1:'Slight pluvial', 2: 'Moderate pluvial',
#                       3:'Severe pluvial', 4:'Extreme pluvial'}
        
        time_ind = 2005-year
#        x,y = m(lon,lat)
        
        # Plot MADA data, PDSI = [time, lat, lon]
        plt.imshow(MADA.variables['PDSI'][time_ind,:,lon_ind].T,extent=(lon.min(),lon.max(),lat.min(),lat.max()),
                                                         interpolation='nearest',cmap=my_cmap) 
#        plt.pcolor(x,y,np.MADA.variables['PDSI'][time_ind,:,:])
        MADA.close() 
        cbar = plt.colorbar()
        plt.clim(-pdsi_lvl,pdsi_lvl)
        cbar.set_ticks(np.arange(-pdsi_lvl,pdsi_lvl+0.1,0.5))
#        cbar.set_ticklabels(pdsi_index[np.arange(-pdsi_lvl,pdsi_lvl+1)])
        
        # Add boundaries from basemap
        m.drawcoastlines()
        m.drawcountries()
    #    m.bluemarble()
    
        # Show plot
        plt.show()


if __name__ == '__main__':
    
    np.set_printoptions(threshold=np.nan)
    
    # ------------------------------------------------------------------------
    year = 2010 # Year to test
    pdsi_lvl = 2 # Make map based on PDSI threshold
    # ------------------------------------------------------------------------
    
#    Open netCDF file
    MADA = sio.netcdf.netcdf_file('MADApdsi.nc', 'r')

    
#    Find available variables in netCDF file
#    for i in MADA.variables:
#        print i
#    print MADA.variables['PDSI'].dimensions
      
    time = MADA.variables['time'][:]
    lat = MADA.variables['lat'][:]
    lon = MADA.variables['lon'][:]
    
        
    # Flip longitudes to map MADA to basemap
    lon_ind = np.zeros(np.size(lon),dtype='int')
    for j in range(34):
        lon_ind[j] = np.int(33-j)
        
    event_count = np.zeros((np.size(time),2))
    # First column of event_count is drought, second is flood
    
    # Produce count of grid cells that exceed threshold PDSI value
    for i in range(np.size(lat)):
        for j in range(np.size(lon)):
            for k in range(np.size(time)):
                if np.isnan(MADA.variables['PDSI'][k,i,j]):
                    continue
                elif MADA.variables['PDSI'][k,i,j] < -pdsi_lvl:
                    event_count[k,0] = event_count[k,0] + 1
                elif MADA.variables['PDSI'][k,i,j] > pdsi_lvl:
                    event_count[k,1] = event_count[k,1] + 1
                    
    print (event_count)
    
    # Time series of extreme event areas - pluvials, droughts
    plt.figure(1)
    plt.plot(time,event_count[:,0],'r-')
    plt.plot(time,event_count[:,1],'b-')
    plt.xlim((1300,2005))
    
    # Time series of total extreme values - pluvials + droughts
    plt.figure(2)
    plt.plot(time,event_count[:,0] + event_count[:,1])
    plt.show()

    # Map of PDSI values for selected year
    Plotter(year)
        
    
    
    
    
    
