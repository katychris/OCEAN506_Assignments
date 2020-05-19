"""
Author: K. Christensen
Date: May 18, 2020
Data: https://nsidc.org/data/seaice_index/archives
                S_seaice_extent_daily_v3.0.csv from

This file is an exploration into Pandas. Using a dataframe, we take the monthly means of the
continuous data as well as the overall monthly means with their standard deviations. Then, we 
plot the data together, also showing just the 2019 monthly sea ice extent with the averages.

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os, sys
sys.path.append(os.path.abspath('./shared'))
import my_module as mymod

# Input / Output Directories
myplace = 'kchris'
in_dir = '../../' + myplace + '_data/'
out_dir = '../../' + myplace + '_output/'

# Set the input and output file paths
csv_file = in_dir + 'S_seaice_extent_daily_v3.0.csv'
out_file = out_dir+'SeaIce_1978_2020.png'

# Read in the csv file skipping the row directly after the headers
df = pd.read_csv(csv_file,skiprows=[1]) 

# Make the column names have no spaces and create a date column to be our index
df.columns = df.columns.str.strip()
df.insert(0,'Date',pd.to_datetime(df[['Year','Month','Day']]))  
df.set_index('Date', inplace=True)

# Drop the unecessary columns and make the extent show the true values
df.drop(['Missing','Source Data'], axis=1, inplace=True)
df['Extent'] = df['Extent'] * 1e6 
df_2019 = df[df['Year']==2019].groupby('Month').mean()
df_2019 = df_2019.rename(columns={'Extent':'2019 Extent'})

# Create a copy of our data and take the continuous monthly mean of the time series
df_avg = df.copy() 
df_avg_co = df_avg.drop('Day',axis=1).groupby(['Year','Month']).mean()

# Create an additional copy and take the overall monthly mean and std of all the data
df_avg_mo = df_avg_co.copy()
df_mo = df_avg_mo.groupby(level='Month')
df_avg_mo = df_mo.mean()
df_avg_mo['std'] = df_mo.std()


# Make the index of the continuous mean into correct dates for easier plotting
y = df_avg_co.index.get_level_values('Year') 
m = df_avg_co.index.get_level_values('Month')  
df_avg_co['Date'] = pd.to_datetime(y * 10000 + 100*m + 15 , format="%Y%m%d") 
df_avg_co = df_avg_co.rename(columns={'Extent':'Monthly Avg.'})
df_avg_co.set_index('Date', inplace=True)
df_avg_mo = df_avg_mo.rename(columns={'Extent':'Average Extent'})

# Plotting Below Here
#------------------------------------------------------------------------------------------
# Set figure paramters
fs = 16
plt.rcParams.update({'font.size': fs})
plt.close('all')

# Create a figure
fig = plt.figure(figsize=(15,8))

# Create a plot that contains the sea ice extent and the continuous monthly averages on top
ax1 = fig.add_subplot(311)
df['Extent'].plot(ax=ax1,color='#000454',linestyle='-',linewidth=3,legend=False,
	title='Antarctic Sea Ice Extent: 1978-2020')
df_avg_co['Monthly Avg.'].plot(ax=ax1,color='#000454',marker='o',mfc='#a4a7e0',
	linestyle='',legend=False)
patches, labels = ax1.get_legend_handles_labels()
ax1.legend(patches, labels,fontsize=fs*0.6,loc='center left', bbox_to_anchor=(1, 0.5))
ax1.set_ylabel('Sea Ice Extent (km$^2$)')

# Create a plot that contains the monthly averages and the std
# Add in the 2019 values for comparison
ax2 = fig.add_subplot(212)
df_avg_mo['Average Extent'].plot(ax=ax2,color = 'k',lw=3,yerr=df_avg_mo['std'],
	capsize=5,title='Antarctic Sea Ice Annual Cycle',xlim=(0,13),
	xticks=range(1,13),ylim=(0,2e7))
ax2.fill_between(df_avg_mo.index.values, 
	df_avg_mo['Average Extent'] - df_avg_mo['std'], 
	df_avg_mo['Average Extent'] + df_avg_mo['std'], 
	alpha=0.5,color='r')
df_2019['2019 Extent'].plot(color='k',linestyle='--',linewidth=2,alpha=0.6,
	legend=False,xlim=(0,13))
patches, labels = ax2.get_legend_handles_labels()
ax2.legend(patches, labels,fontsize=fs*0.6,loc='lower right')
ax2.set_ylabel('Sea Ice Extent (km$^2$)')
ax2.grid()

# Save the figure
fig.savefig(out_file)
plt.rcdefaults()
