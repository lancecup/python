import numpy as np 

my_arr = np.arange(1_000_000)

my_list = list(range(1_000_000))

# %timeit my_arr2 = my_arr * 2
# %timeit my_list2 = [x * 2 for x in my_list]

# ============================================================================ #
#                NumPy ndarray: A Multidimensional Array Object                #
# ============================================================================ #

# this ndarray is a fst, flexible containers for large datasets

data = np.array([[1.5, -0.1, 3], [0, -3, 6.5]])
data 

data * 10

data + data 

type(data)
data.shape
data.dtype 

# ----------------------------- Creating ndarrays ---------------------------- #
# easiest way to make an array is array() 
data1 = [6, 7.5, 8, 0, 1]

arr1 = np.array(data1)
arr1

# nested sequences will be converted into a multidimensional array
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]

arr2 = np.array(data2)
arr2

# data2 was a list of lists, so arr2 has two dimensions
arr2.ndim 
arr2.shape 

arr1.dtype 
arr2.dtype

# alternatively, can use np.zeros or np.ones to make an array of 0s or 1s
np.zeros(10)

np.zeros((3, 6))

np.empty((2, 3, 2)) # populates with nonzero garbage values

# np.arange is an array valued version of range()

np.arange(15)

# important numpy array creation functions
# array - convert input data to an ndarray 
# asarray - convert input to ndarray but dont copy if the input is already an ndarray
# arange - like the builtin range but returns an ndarray instead of a list
# ones, ones_like - makes an array of 1s; ones_like takes another array and makes a ones array of the same shape
# zeros .
# empty .
# full - produces an array with all values set ot the fill value
# eye, identity - creates an nxn identity matrix 

# -------------------------- Data Types for ndarrays ------------------------- #

arr1 = np.array([1, 2, 3], dtype = np.float64)
arr1 = np.array([1, 2, 3], dtype = np.int32)
arr1.dtype
arr2.dtype 

# you can explicitly cast an array from one data type to another using astype
arr = np.array([1, 2, 3, 4, 5])
arr.dtype
float_arr = arr.astype(np.float64)
# astype always creates a new array even if the new data type is the same as the old data type

# ----------------------- Arithmetic with NumPy Arrays ----------------------- #
arr = np.array([[1., 2., 3.], [4., 5., 6.]])

arr 

arr * arr
arr - arr
1 / arr 

arr ** 2

arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
arr2 

arr2 > arr

# ------------------------ Basic Indexing and Slicing ------------------------ #
arr = np.arange(10)
arr

arr[5]
arr[5:8]

arr[5:8] = 12

# array slices are views of the original array, not separate copies
arr_slice = arr[5:8]
arr_slice
arr_slice[1] = 12345
arr

arr_slice[:] = 64
arr

# if you want a copy, you will need to explicitly copy() it

# in 2d array, the elements at each index are no longer scalars but one-dimensional arrays
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

arr2d[2]
# individual eleements can be accessed recursively or a comma separated list
arr2d[0][2] 
arr2d[0, 2]

# in higher dimensions:
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
arr3d

arr3d[0]

old_values = arr3d[0].copy()
arr3d[0] = 42
arr3d 

arr3d[0] = old_values
arr3d

arr3d[1, 0]

x = arr3d[1]
x 
x[0]

# indexing with slices