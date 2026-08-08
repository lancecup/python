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
# can be sliced using familiar syntax
# object[row, column] -- object[first_interested_row:last_interested_row: ] all cols
arr2d

arr2d[:2] # select first two rows 
arr2d[:2, 1:]
lower_dim_slice = arr2d[1, :2]
lower_dim_slice.shape
arr2d[:2, 2]
arr2d[:, :2] # dont forget when indexing with : , the end is actually up to end-1
# so ^ ends on the 2nd col, now compared to the 3rd col


# ----------------------------- Boolean Indexing ----------------------------- #

names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
data = np.array([[4, 7], [0, 2], [-5, 6], [0, 0], [1, 2], [-12, -4], [3, 4]])

names
data 

# suppose that each name corresponds to a row

data[names == "Bob"] # row 1 and 4

# here we select from the array with names == "Bob"
data[names == "Bob", 1:] # excludes first col
data[names == "Bob", 1]

# negation
names != "Bob"
~(names == "Bob")
data[~(names == "Bob")]

cond = names == "Bob"
data[~cond]

mask = (names == "Bob") | (names == "Will")
mask
data[mask]

# selecting data from an array by boolean indexing always creates a copy of the data

# can also set values with boolean arrays - convert negative to 0
data[data < 0] = 0
data 

data[names != "Joe"] = 7

data 

# ------------------------------ Fancy Indexing ------------------------------ #
arr = np.zeros((8,4))
for i in range(8):
    arr[i] = i 
arr 
# we can index a subset of rows by indexing a list of the row numbers we want
arr[[4, 3, 0, 6]]

# this gets the last 3rd (5th row), last 5th (3rd row), and last 7th (2nd row)
arr[[-3, -5, -7]]

arr = np.arange(32).reshape((8, 4))
arr 

arr[[1, 5, 7, 2], [0, 3, 1, 2]]

arr[[1, 5, 7, 2], [0, 3, 1, 2]] = 100
arr

# -------------------- Transposing Arrays / Swapping Axes -------------------- #
arr = np.arange(15).reshape((3, 5))
arr
arr.T

# inner matrix product -- np.dot 
arr = np.array([[0, 1, 0], [1, 2, -2], [6, 3, 2], [-1, 0, -1], [1, 0, 1]])
arr

np.dot(arr.T, arr)
arr.T @ arr

# alternatively, you can use the swapaxes method of ndarrays
arr.swapaxes(0, 1)

# ============================================================================ #
#                                  Pseudo RNG                                  #
# ============================================================================ #

# np.random module to efficiently generate whole arrays of sample values from prob dists
# ex. 4x4 array of samples from standard normal dist

samples = np.random.standard_normal(size = (4,4))
samples

# pythons built in random module only samples one value at a time
rng = np.random.default_rng(seed = 12345)
data = rng.standard_normal((2, 3))
type(rng)

# rng methods
# permutation - returns a random permutation of a sequence
# shuffle - randomly permutes a sequence in place
# uniform - draws samples from a uniform dist
# integers - draws random integers from a given low-to-high range
# standard_normal - draws from standard normal dist
# binomial - draws from binomial dist
# normal - normal dist
# beta - beta dist
# chisquare - chisquare dist 
# gamma - gamma dist

# ============================================================================ #
#            Universal Functions: Fast Element-Wise Array Functions            #
# ============================================================================ #

# a function that performs element wise operations on data in ndarrays

# unary ufunctions take one array and returns one array
# e.g. np.sqrt or np.exp 

arr = np.arange(10)
arr

np.sqrt(arr) 
np.exp(arr)

# binary ufunctions takes two and returns a single array
# np.add or np.maximum takes two array
x = rng.standard_normal(8)
y = rng.standard_normal(8)
x 
y
np.maximum(x, y) # element-wise max
np.add(x, y)

# a ufunc can return multiple arrays
# e.g. np.modf - returns the fractional and integral parts of a floating point
arr = rng.standard_normal(7) * 5
arr 

remainder, whole_part = np.modf(arr)
remainder
whole_part

whole_part.astype(np.int32)

arr 

# ufuncs accept an out argument that lets you assign the results to an existing array
new_arr = np.zeros_like(arr)
np.add(arr, 1)
np.add(arr, 1, out = new_arr)
new_arr

# some unary ufuncs
# abs, fabs - compute the absolute value element wise
# sqrt - compute the square root 
# square - compute the square of each element 
# exp - compute e^x of each element 
# log, log10,log2, log1p - log base e, log base 10, log base 2, ln(1 + x) the element
# sign - compute the sign of each element
# ceil - compute the celing of each element (smallest integer greater than or equal to that number)
# floor - compute the floor ""
# rint - round elements to the nearest integer
# modf - return the fractional and integral parts of array as separate
# isnan - return the boolean array indicating whether each value is NaN
# isfinite, isinf - returns boolean array if the element is finite or infinite
# trigonometry - cos, cosh, sin, sinh, tan, tanh, arccos, arccosh, arcsin, arcsinh, arctan, arctanh
# logical_not - compute the truth value of not x, element wise

# some binary ufuncs
# add, subtract, multiply, divide, floor_divide
# power - raise elements in the first array to powers indicated in second array
# maximum, fmax - max (fmax ignores NaN)
# minimum, fmin - "
# mod - element wise modulus (remainder of division)
# copysign - copy the sign of values in the second array to values in the first array
# greater, great_equal, less, less_equal, equal, not_equal - yields boolean array
# logical_and - AND
# logical_or - OR 
# logical_xor - XOR 

# ============================================================================ #
#                    Array-Oriented Programming with Arrays                    #
# ============================================================================ #

# e.g. sqrt(x^2 + y^2) // np.meshgrid takes two one-dimensional arrays and produces 2d matrices corresponding to all pairs of (x,y)
points = np.arange(-5, 5, 0.01)
xs, ys = np.meshgrid(points, points)

z = np.sqrt(xs ** 2 + ys ** 2)
z

# ------------- Expressing Conditional Logic as Array Operations ------------- #
# np.where is a vectorized version of x if condition else y

xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
result

# alternatively, use np.where
result = np.where(cond, xarr, yarr)
result

# the second and third arguments don't need to be arrays, they can be scalars
# you can use where to produce a new array of values based on another array
# suppose you had a matrix of randomly gneerated data, and you want to replae all positive numbers with 2 and negative with -2
arr = rng.standard_normal((4,4))
arr

arr > 0

np.where(arr > 0, 2, -2)
np.where(arr > 0, 2, arr)

# ------------------- Mathematical and Statistical Methods ------------------- #

arr = rng.standard_normal((5, 4))
arr
arr.mean()
np.mean(arr)
arr.sum()

arr.mean(axis = 1) # axis = 1 does it by row, across the columns
arr.sum(axis = 0) # axis = 0 does it by col, down the rows

# other methods like cumsum and cumprod don't aggregate and instead make an array of intermediate results
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7])
arr.cumsum()

# in multidimensional arrays, accumulation functions return an array of the same size
arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
arr 

arr.cumsum(axis = 0) 
arr.cumsum(axis = 1)

# basic array statistical methods
# sum - sum of all the elements in the array or along an axis
# mean - arithmetic mean
# std, var - standard deviation and variance
# min, max
# argmin, argmax - indices of minimum and maximum elements
# cumsum - cumulative sum of elements
# cumprod - cumulative product of elements

# ------------------------ Methods for Boolean Arrays ------------------------ #

# sum counts True values in a Boolean array
arr = rng.standard_normal(100)
(arr > 0).sum()
(arr <= 0).sum()

# any and all are useful for boolean arrays
bools = np.array([False, False, True, False])
bools.any() #  if there's any true
bools.all() # if all of them are true

# ---------------------------------- Sorted ---------------------------------- #
arr = rng.standard_normal(6)
arr 
arr.sort()

# you can sort each one dimensional section of values in a multidemnsional array in place along an axis
arr = rng.standard_normal((5, 3))
arr 
arr.sort(axis = 0) # sorts the values within each column
arr 

arr.sort(axis = 1) # sorts across each row
arr

# np.sort returns a sorted copy of the array
arr2 = np.array([5, -10, 7, 1, 0, -3])
sorted_arr2 = np.sort(arr2)
sorted_arr2

# ------------------------ Unique and Other Set Logic ------------------------ #
# np.unique returns the sorted unique values in an array

names = np.array(["Bob", "Will", "Joe", "Bob", "Will", "Joe", "Joe"])
np.unique(names)
ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
np.unique(ints)

# contrast this to the base alternative
sorted(set(names))

# numpy alternative is faster 

# another function, np.in1d tests membership of the values in one array in another
values = np.array([6, 0, 0, 3, 2, 5, 6])

np.in1d(values, [2, 3, 6])
# checking if 2, 3, 6 is in the values array

# array set operations
# unique(x) - compute the sorted, unique elements in x
# intersect1d(x, y) - compute the sorted, common elements in x and y
# union1d(x, y) - compute the sorted union of elements
# in1d(x, y) - compute a boolean array indicating whether each element of x is contained in y
# setdiff1d(x, y) - set difference, elements in x that are not in y
# setxor1d(x, y) - set symmetric differences ; xor

# ============================================================================ #
#                       File Input and Output with Arrays                      #
# ============================================================================ #

arr = np.arange(10)
np.save("some_array", arr) # stored in .npy
np.load("some_array.npy")

# you can save multiple arrays in an uncompressed archive with np.savez
np.savez("array_archive.npz", a = arr, b = arr)

arch = np.load("array_archive.npz")
arch["a"]
arch["b"]

np.savez_compressed("arrays_compressed.npz", a = arr, b = arr)

# ============================================================================ #
#                                Linear Algebra                                #
# ============================================================================ #

# element-wise product is *
# matrix multiplication is either dot() or @ 

x = np.array([[1., 2., 3.], [4., 5., 6.]])

y = np.array([[6., 23.], [-1, 7], [8, 9]])

x 
y 
x.dot(y)

# this is equivalent to np.dot(x, y)

x.dot(y)
np.dot(x, y)

x @ np.ones(3)

# numpy.linalg has a standard set of matrix decompositions (e.g. inverse and determinant)

from numpy.linalg import inv, qr

X = rng.standard_normal((5, 5))

mat = X.T @ X

inv(mat) 

mat @ inv(mat)

# numpy.linalg functions
# diag - diagonal elements of array
# dot - matrix multiplication
# trace - sum of the diagonal elements
# det - matrix determinant
# eig - eigenvalues and eigenvectors of square matrix
# inv - inverse of square matrix
# pinv - Moore-Penrose pseudoinverse of a matrix
# qr - qr decomposition
# svd - singular value decomposition
# solve - solve the linear system Ax = b 
# lstsq - least square solution to Ax = b

# ----------------------------- Ex. Random Walks ----------------------------- #
import random 
import matplotlib.pyplot as plt
position = 0 
walk = [position]
nsteps = 1000
for _ in range(nsteps):
    step = 1 if random.randint(0, 1) else -1 
    position += step 
    walk.append(position)

plt.plot(walk[:100])

nsteps = 1_000
rng = np.random.default_rng(seed = 12345)
draws = rng.integers(0, 2, size = nsteps)
steps = np.where(draws == 0, 1, -1)
walk = steps.cumsum()

walk.min()
walk.max()

# the first crossing time, first time it reached 10
(np.abs(walk) >= 10).argmax()

# simulating many random walks

nwalks = 5_000
nsteps = 1_000
draws = rng.integers(0, 2, size=(nwalks, nsteps)) # 0 or 1
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(axis = 1)
walks
walks.max()
walks.min()

# out of these walks, let's compute the min crossing time to 30 or -30
hits30 = (np.abs(walks) >= 30).any(axis = 1)
hits30
hits30.sum() # number that hit 30 or -30 

# we can use this boolean array to select the rows of walks that actually cross 30 or -30 (call argmax across axis 1)
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(axis = 1)
crossing_times 

crossing_times.mean() # average min crossing times

draws = 0.25 * rng.standard_normal((nwalks, nsteps))
draws 