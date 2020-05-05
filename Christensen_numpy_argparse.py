'''

This code is for the numpy & argparse assignment for OCEAN 506.
Author: K. Christensen
Due: 11:59:00 May 4, 2020

Input Arguments
---------------
-a : determines array sizes, must be divisible by 100
-p : determines if the arrays and their manipulations will be printed

'''

# Import key packages
import numpy as np
import argparse
import pickle
import sys, os
from datetime import datetime

# Import our package for creating directories if needed
sys.path.append(os.path.abspath('./shared'))
import my_module as mymod
from importlib import reload
reload(mymod)

# make sure the output directory exists
this_dir = os.path.abspath('.').split('/')[-1]
this_parent = os.path.abspath('.').split('/')[-2]
out_dir = '../' + this_dir + '_output/'
print('Creating ' + out_dir + ', if needed','\n')
mymod.make_dir(out_dir)

# Setting up argparse
#------------------------------------------------------------------------
# Make sure that the argument is a boolean
def boolean_string(s):
    # this function helps with getting Boolean input
    if s not in ['False', 'True']:
        raise ValueError('Not a valid boolean string')
    return s == 'True' # note use of ==

# This will cause an error if the value input is not divisible by 100
def hundred_in(s):
    if int(s) % 10 != 0:
        raise ValueError('Not divisible by 10.')
    return int(s)


# create the parser object
parser = argparse.ArgumentParser()

# add the argument for getting the array shapes
parser.add_argument('-a', '--tens_val', default=30, type=hundred_in)
parser.add_argument('-p','--printing_arrays',default=False,type=boolean_string)

# get the arguments
args = parser.parse_args()
 

# Creating and manipulating arrays
#------------------------------------------------------------------------
# create a variable based on the input
sz = args.tens_val
print('Number of Columns:',int(sz/10),'\n')

# create arrays based on the input
# the arrays will always have 10 rows
a1 = np.arange(0,sz,1).reshape((10,int(sz/10)))  
a2 = np.linspace(0,1,sz).reshape((10,int(sz/10)))
a3 = np.random.rand(10,int(sz/10))

# square the first array
a1_s = a1**2

# multiply the second two together
b = a2*a3

# take the mean of the second array
a2_mean = np.mean(a2)

# take the mean of the third array
a3_mean = np.mean(a3)

# take the column mean of the third array
a3_colmean = np.mean(a3,axis=0)

# create a mask for the second array
mask = a2>=0.5

# multiply a3 by 100
c = a3*100


if args.printing_arrays:
	print('Array a1:\n', a1,'\n')
	print('Array a2 (linear increase):\n', a2,'\n')
	print('Array a3 (random values):\n', a3,'\n')
	print('a1**2:\n',a1_s,'\n')
	print('a2*a3: \n', b,'\n')
	print('a2 average (should be 0.5):\n',a2_mean)
	print('a3 average:\n',a3_mean,'\n')
	print('a3 average of each column:\n',a3_colmean,'\n')
	print('a2 mask >0.5:\n',mask,'\n')
	print('a3*100:\n',c,'\n')
else:
	print('Arrays have been created and maniulated:')
	print('To see the full results, run the code with argument -p True\n')



# Using pickle to save and reload data
#------------------------------------------------------------------------
print('Saving a3 column averages...')
# save it as a pickle file
now = datetime.now()
dt = now.strftime('%Y_%m_%d_%H%M')
out_fn = out_dir + 'average_random_columns_'+dt+'.p'
pickle.dump(a3_colmean, open(out_fn, 'wb')) # 'wb' is for write binary

# read the array back in
rel = pickle.load(open(out_fn, 'rb')) # 'rb is for read binary

print('The average column values are:')
print(rel)


