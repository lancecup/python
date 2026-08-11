import numpy as np
import pandas as pd 

# ============================================================================ #
#                          Intro to pd Data Structures                         #
# ============================================================================ #``

# ---------------------------------- Series ---------------------------------- #

# one dimensional array-like object containing a sequence of values of the same type
obj = pd.Series([4, 7, -5, 3])
obj 

obj.array # pandas array which is a np.array but with a special extension
obj.index 

obj2 = pd.Series([4, 7, -5, 3], index = ["d", "b", "a", "c"])
obj2 
obj2.index 

# you can use labels in the index when selecting single values
obj2["a"]
obj2["d"] = 6
obj2[["c", "a", "d"]]

# cn filter with a boolean array, scalar multiplication, or math functions will preserve indices
obj2[obj2 > 0]
obj2 * 2
np.exp(obj2)

# can also think of a series as a fixed length ordered dictionary that maps index to data
# can be used where you might use a dictionary
"b" in obj2
"e" in obj2

# can convert dictionary into pandas series
sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
obj3 = pd.Series(sdata)
obj3
obj3.to_dict()

# you can explicitly list which keys you want in the series by passing an index
states = ["California", "Ohio", "Oregon", "Texas"]
obj4 = pd.Series(sdata, index = states)
obj4 

# isna and notna are used to detect missing data
pd.isna(obj4)
pd.notna(obj4)
obj4.isna()
obj4.isna().mean()

obj3 
obj4 
obj3 + obj4  # automatically aligns by index

obj4.name = "population"
obj4.index.name = "state"

obj4 

# a series index can be altered in place by assignment
obj 
obj.index = ["Bob", "Steve", "Jeff", "Ryan"]
obj 

# -------------------------------- Data Frame -------------------------------- #
# rectangular table of data

# one of the most common ways is to convert a dictionary of equal-length lists or numpy arrays
data = {"state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
frame 

frame.head() # first 5 rows
frame.tail() # last 5 rows
pd.DataFrame(data, columns = ["year", "state", "pop"]) # specify order of cols

# if you pass a column not in the dictionary, it will all be NA
frame2 = pd.DataFrame(data, columns = ["year", "state", "pop", "debt"])
frame2 
frame2.columns # checking cols

# you can get a col using indexing or dot notation
frame2["state"]
frame2.state

# rows can be retrieved by position or name with iloc and loc respectively
frame2.loc[1]
frame2.iloc[2]

# columns can be modified by assignment
frame2["debt"] = 16.5
frame2 
frame2["debt"] = np.arange(6.)
frame2 

# when assigning lists or arrays to a column, the value's length must match the length of the df
val = pd.Series([-1.2, -1.5, -1.7], index = [2, 4, 5])
frame2["debt"] = val
frame2 

# assigning a column that doesn't exist will create a new column

frame2["eastern"] = frame2["state"] == "Ohio"
frame2 

# can delete columns with del 
del frame2["eastern"]
frame2.columns 

# the column returned from indexing a df is a view, not a copy so any change alters the original

# another common form of data is a nested dictionary of dictionaries
populations = {"Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6}, 
               "Nevada": {2001: 2.4, 2002: 2.9}}

# pandas will interpret the outer dictionary keys as the columns and the inner keys as the row indices
frame3 = pd.DataFrame(populations)
frame3 
frame3.T # transposes the dataframe
# not that this destroys the column types

pd.DataFrame(populations, index = [2001, 2002, 2003])

pdata = {"Ohio": frame3["Ohio"][:-1], "Nevada": frame3["Nevada"][:2]}
pd.DataFrame(pdata)

# possible data inputs to DataFrame()
# 2d ndarray
# dictionary of arrays, lists, or tuples - each sequence becomes a column
# numpy structured arrays - treated as above
# dictionary of series - each value becomes a column
# dictionary of dictionaries - each inner dictionary becomes a column 
# list of dictionaries or series = each item becomes a row

# if a df's index and columns have their name attributes set, these will be displayed
frame3.index.name = "year"
frame3.columns.name = "state"
frame3

# can convert df to ndarray with to_numpy()
frame3.to_numpy()
frame2.to_numpy()

# ------------------------------- Index Objects ------------------------------ #
# index objects are responsible for holding the axis labels (including col names) and other metadata (axis name or names)
obj = pd.Series(np.arange(3), index = ["a", "b", "c"])

index = obj.index 
index 
index[1:]

index[1] = "d" # index objects are immutable

labels = pd.Index(np.arange(3))
labels 

obj2 = pd.Series([1.5, -2.5, 0], index = labels)
obj2 

obj2.index is labels 

# an index also behaves like a fixed-size set
frame3 

frame3.columns 
"Ohio" in frame3.columns 

2003 in frame3.index 

test = pd.Index(["foo", "foo", "bar", "bar"])
test2 = pd.Index(["foo", "foo", "xd"])
test3 = pd.Index(["foo", "bar"])

test.difference(test2)
test.intersection(test2)
test3.isin(test)
test2.delete(1)
test.drop("foo")

test.insert(1, "foo") # position 

# Some Index methods and properties
# append() - concatenate with additional index objects producing a new index
# difference() - set difference as an index 
# intersection() - set intersection
# union() - set union
# isin() - boolean array indicating whether each value is contained in the collection
# delete(i) - new index with element at index i deleted
# drop() - delete but with name
# insert() - new index by inserting element at index i
# is_monotonic() - returns true if each element is >= to the previous element
# is_unique() - returns true if the index has no duplicate values
# unique() - compute the array of unique values in the index 

# -------------------------- Essential Functionality ------------------------- #

### Reindexing
# reindex() - creates a new object with the values rearranged to align with the new index
obj = pd.Series([4.5, 7.2, -5.3, 3.6], index = ["d", "b", "a", "c"])
obj 

obj2 = obj.reindex(["a", "b", "c", "d", "e"])
obj2 

# for ordered data like time series, you might want to interpolate some values when reindexing
# method option lets you do this with ffill - forward fills
obj3 = pd.Series(["blue", "purple", "yellow"], index = [0, 2, 4])
obj3 

obj3.reindex(np.arange(6), method = "ffill")

# reindex can alter the index, cols, or both
frame = pd.DataFrame(np.arange(9).reshape((3, 3)),
                     index = ["a", "c", "d"],
                     columns = ["Ohio", "Texas", "California"])
frame 

frame2 = frame.reindex(index = ["a", "b", "c", "d"]) # reindexes rows by default
frame2 # b's are nans

states = ["Texas", "Utah", "California"]
# can reindex via columns with columns = or axis = "columns"
frame.reindex(columns = states)
frame.reindex(states, axis = "columns")

# reindex function arguments
# labels - new sequence to use as an index (can be index instance or any sequence data structure)
# index - use the passed sequence as the new index labels
# columns - use the passed sequence as the new column labels
# axis - the axis to reindex , .reindex(index, axis = y)
# method - interpolation fill method - "ffill" forward fill - "bfill" fills backward
# fill_value - substitute value to use when introducing missing data by reindexing - fill_value = "missing" to have null values in the result
# limit - when forwardfilling or backfilling the maximum size gap to fill
# tolerance - when forward filling, the maximum size gap to fill for inexact matches
# level - match simple index on level of MultiIndex
# copy - if true, always copy underlying data even if the new index is equivalent to the old index ; if falsem don't copy the data when the indexes are equiv

# you can also reindex by using loc - only works if new index values are already in the old
# essentially filtering rows and selecting cols
frame.loc[["a", "d", "c"], ["California", "Texas"]]

### Dropping Entries from an Axis
# dropping entries from an axis with .drop() will return a new object 
obj = pd.Series(np.arange(5), index = ["a", "b", "c", "d", "e"])
obj 
new_obj = obj.drop("c")
obj.drop(["d", "c"])

data = pd.DataFrame(np.arange(16).reshape((4, 4)), 
                    index=["Ohio", "Colorado", "Utah", "New York"], 
                    columns=["one", "two", "three", "four"])
data 

data.drop(index = ["Colorado", "Ohio"]) # remove rows
data.drop(columns = ["two"]) # remove cols

# you can also drop cols with axis = 1 or axis = "columns"
data.drop("two", axis = 1)
data.drop(["one", "three"], axis = "columns")

### Indexing, Selection, Filtering
# indexing obj[...] is analogous to np array indexing but can also call by index names
obj = pd.Series(np.arange(4.), index=["a", "b", "c", "d"])
obj 
obj["b"]
obj[1]
obj[2:4]
obj[["b", "a", "d"]]
obj[[1, 3]]
obj[obj < 2]

# we prefer loc to select index values because of the different treatment of integers when indexing with []
obj.loc[["b", "a", "d"]]

obj1 = pd.Series([1, 2, 3], index = [2, 0, 1])
obj2 = pd.Series([1, 2, 3], index = ["a", "b", "c"])
obj1 
obj2 
obj1[[0, 1, 2]]
obj2[[0, 1, 2]]

# obj2.loc[[0,1]] - this fails since the index does not contain integers
# iloc indexes exclusively with integers 
obj1.iloc[[0, 1, 2]]
obj2.iloc[[0, 1, 2]]

# you can also slice with labels but slicing includes the endpoints
obj2.loc["b":"c"]

obj2.loc["b":"c"] = 5
obj2 

# don't forget, loc, and iloc uses square brackets 
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])
data 
data["two"]
data[["three", "one"]]

# passing a single element or a list to the [] operator selects columns
data[:2]
data[data["three"] > 5]

data["one"]

# another use case is indexing with a boolean df 
data < 5
data[data < 5] = 0 # use it to assign based on condition
data[data["one"] < 5] # selects rows where this is true

### Selection on DataFrame with loc and iloc
data 
data.loc["Colorado"]
data.loc[["Colorado", "New York"]]
data.loc["Colorado", ["two", "three"]]
data.iloc[2] 
data.iloc[[2, 1]]
data.iloc[[1, 2], [3, 0, 1]]
data.loc[: "Utah", "two"]
data.iloc[:, :3][data.three > 5] # first gets up to 3rd row, then filters rows if the three col values > 5

# boolean arrays can be used with loc but not iloc
data.loc[data.three >= 2]

# indexing options with dfs
# df[column] - select single column or sequence of columns from the df
# df[boolean_array / condition] - filters rows
# df[x:y, a:b] - slice
# df.loc[rows] - select single row or subset of rows by label
# df.loc[:, cols] - select single column or subset of columns
# df.loc[rows, cols] - select rows and cols by label
# df.iloc[rows] - select rows by integer positions
# df.iloc[:, cols] - select cols by integer position
# df.iloc[rows, cols] - select rows and cols by integer position
# df.at[row, col] - select a single scalar value by row and column label
# df.iat[row, col] - select a single scalar value by row and column position
# reindex - select either rows or columns by labels

# potential pitfalls
ser = pd.Series(np.arange(3.))
ser 
# ser[-1] # error 
# when we have a noninteger index, there is no ambiguity
ser2 = pd.Series(np.arange(3.), index = ["a", "b", "c"])
ser2[-1]

# if you have an axis index containing integers, data selection will always be label oriented
ser.iloc[-1]

# slicing with integers is always integer oriented
ser[:2]

# Chained indexing pitfalls
# we showed that we can assign to a col or row by label or position
data.loc[:, "one"] = 1
data 
data.iloc[2] = 5
data.loc[data["four"] > 5] = 3
data 

# if you try to chain, you might encounter a SettingWithCopyWarning error
# you are trying to modify a temporary value (the nonempty result of data.loc[data.three == 5]) instead of the original dataframe data
data.loc[data.three == 5]["three"] = 6


# the fix is to rewrite the chained assignment using a single loc operation
data.loc[data.three == 5, "three"] = 6
data 

# ----------------------- Arithmetic and Data Alignment ---------------------- #
# when you add objects, if any index pairs are not the same, the index in the result will be the union of the index pairs
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=["a", "c", "e", "f", "g"])

s1 
s2 

s1 + s2 
# missing values are introduced in indices that don't overlap which propagate in arithmetic computations
# pandas matches data by both the row names and the column names before doing an operation

# for dfs, alignment is dont on both rows and cols
df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list("bcd"),
                   index=["Ohio", "Texas", "Colorado"])

df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list("bde"),
                   index=["Utah", "Ohio", "Texas", "Oregon"])

df1
df2 

df1 + df2 
# since c and e are not in both dfs, they are missing
# the same holds for the rows with labels not common to both

# if you add df objects with no col or row labels in common, the result will contain all nulls
df1 = pd.DataFrame({"A": [1, 2]})
df2 = pd.DataFrame({"B": [3, 4]})
df1 
df2 

df1 + df2 

## Arithmetic methods with fill values
# you might want to fill with a special value (e.g. 0)
df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)), columns=list("abcd"))

df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)), columns=list("abcde"))

df2.loc[1, "b"] = np.nan
df1
df2 
df1 + df2 # many nans

# can use the add method on df1 with fill_value 
df1.add(df2, fill_value=0)
1 / df1 
df1.rdiv(1)

# when reindexing a series or dataframe you can specify a different fill value
df1.reindex(columns = df2.columns, fill_value = 0)

## Flexible arithmetic methods (r prefix reverses the arguments)
# add, radd - addition
# sub, rsub - subtratction
# div, rdiv - division 
# floordiv, rfloordiv - floor division
# mul, rmul - multiplication
# pow, rpow - exponentiation

# operations between dfs and series
arr = np.arange(12.).reshape((3, 4))
arr 
arr[0] 
arr - arr[0] 

# the subtraction is performed by row - broadcasting
frame = pd.DataFrame(np.arange(12.).reshape((4, 3)), 
                     columns=list("bde"), 
                     index=["Utah", "Ohio", "Texas", "Oregon"])

series = frame.iloc[0]
series 

# arithmetic between df and series matches the index of the series on the cols of the df, broadcasting down the rows
frame - series 

# if there's no index value in either df cols or series index, the objects will be reindexed to form the union
series2 = pd.Series(np.arange(3), index = ["b", "e", "f"])
series2 
frame + series2

# to broadcast over columns, matching on the rows, you have to use arithmetic methods and specify to match over the index 
series3 = frame["d"]
frame 
series3 
frame.sub(series3, axis = "index")
# the axis that we put here is the axis to match on, so we match on df's row index and broadcast across cols


# --------------------- Function Application and Mapping --------------------- #
# np ufuncs work with pandas objects

frame = pd.DataFrame(np.random.standard_normal((4, 3)), 
                     columns = list("bde"),
                     index = ["Utah", "Ohio", "Texas", "Oregon"])
frame 
np.abs(frame)

# we typically want to apply a function on 1D arrays to each col or row
# to do this, use apply()

def f1(x):
    return x.max() - x.min()
frame.apply(f1)

# f1 computes the difference of max and min of a series is invoked on each col of frame
# if axis = "columns", it will be invoked per row instead
frame.apply(f1, axis = "columns")

# the function passed to apply can also return a series
def f2(x): 
    return pd.Series([x.min(), x.max()], index = ["min", "max"])
frame.apply(f2)

# element-wise functions can be used too with map()
def my_format(x):
    return f"{x:.2f}"
frame.map(my_format)

frame["e"].map(my_format)

# ---------------------------- Sorting and Ranking --------------------------- #
# sorting a dataset by a variable

# to sort by row or column label, use sort_index
obj = pd.Series(np.arange(4), index=["d", "a", "b", "c"])
obj 
obj.sort_index()

frame = pd.DataFrame(np.arange(8).reshape((2, 4)), 
                     index=["three", "one"], 
                     columns=["d", "a", "b", "c"])
frame 
frame.sort_index()
frame.sort_index(axis = "columns")

# can sort in descending order too
frame.sort_index(axis = "columns", ascending = False) 

# sorting series by values, use sort_values()
obj = pd.Series([4, 7, np.nan, -3, 2])
obj.sort_values() 

# missing values are sorted to the end by default
# missing values can be sorted to the start instead of the end 
obj.sort_values(na_position = "first")

# sort by col 
frame = pd.DataFrame({"b": [4, 7, -3, 2], "a": [0, 1, 0, 1]})

frame

frame.sort_values("b", ascending = False)
frame.sort_values(["a", "b"], ascending = False)

obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
obj.rank() # assigns ranks from one through n starting from the lowest value
# ranks can also be assigned according to the order in which they're observed in the data
obj.rank(method = "first")

# ranks can be descending as well
obj.rank(ascending = False)

# ranks work for rows or cols as well 
frame = pd.DataFrame({"b": [4.3, 7, -3, 2], 
                      "a": [0, 1, 0, 1], 
                      "c": [-2, 5, 8, -2.5]})
frame 
frame.rank(axis = "columns")
frame.rank(axis = "rows")

# rank methods
# average - default
# min - use the minimum rank for the whole group
# max - use the max rank 
# first - assign ranks in the order the values appear
# dense - like min but always increase by 1 between groups rather than the number of equal elements in a group

# -------------------- Axis Indexes with Duplicate Labels -------------------- #
obj = pd.Series(np.arange(5), index=["a", "a", "b", "b", "c"])
obj 

# can use is_unique on index to see if labels are unique 
obj.index.is_unique 

obj["a"]

obj["c"]

df = pd.DataFrame(np.random.standard_normal((5, 3)), 
                  index=["a", "a", "b", "b", "c"])

df 
df.loc["b"]
df.loc["c"] 

# ============================================================================ #
#               Summarizing and Computing Descriptive Statistics               #
# ============================================================================ #

df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],
                   [np.nan, np.nan], [0.75, -1.3]],
                   index=["a", "b", "c", "d"],
                   columns=["one", "two"])
df 
df.sum() 
df.sum(axis = "columns") # colsums
# if there are NA, the sums are na, so can skipna option
df.sum(axis="index", skipna = False)
df.sum(axis = "columns", skipna = False) 

# some aggregations require at least one non-NA to get a result 
df.mean(axis = "columns")

# options for reduction methods
# axis - axis to reduce over - index for rows, columns for columns
# skipna - exclude nans
# level - reduce grouped by level if the axis is hierarchically indexed

# some methods (e.g. idxmin, idxmax) return indirect stats like the index value where the min or max are attained
df.idxmax()

df.cumsum() # accumulations

# some methods are neither reductions nor accumulations, e.g. describe
df.describe()

# on non-numeric data, describe produces alternative summary stats
obj = pd.Series(["a", "b", "c" , "a"] * 4)
obj.describe()

# descriptive and summary statistics
# count - number of non-NA
# describe - summary stats
# min, max - min and max values
# argmin, argmax - index locations of max and min - not available on dfs
# idxmin, idxmax - index labels at which min or max is obtained
# quantile - sample quantile ranging from 0 to 1 
# sum - sum of values
# mean - mean
# median
# mad - mean absolute deviation from mean
# prod - prod of all values
# var - sample variance
# std - sd of values
# skew - skewness of values
# kurt - kurtosis of values
# cumsum - cumulative sum
# cummin, cummax - cumulative min or max
# cumprod - cumulative prod 
# diff - first difference
# pct_change 

# ------------------------ Correlation and Covariance ------------------------ #
price = pd.read_pickle("examples/yahoo_price.pkl")

volume = pd.read_pickle("examples/yahoo_volume.pkl")


returns = price.pct_change()
returns.tail()

# Series corr computes the correlation of the overlapping, non-NA, aligned-by-index values in two series
returns["MSFT"].corr(returns["IBM"])
returns["MSFT"].cov(returns["IBM"])

# df corr and cov return a full cor/cov matrix
returns.corr()
returns.cov()

# df's corrwith lets you compute pair-wise corr between df's cols or rows with another series or df
returns.corrwith(returns["IBM"])
# passing a series returns a series
# passing a df computes teh corr for matching col names
returns.corrwith(volume)
# axis = "columns" does row by row instead

# ------------------ Unique Values, Value Counts, Membership ----------------- #
obj = pd.Series(["c", "a", "d", "a", "a", "b", "b", "c", "c"])
uniques = obj.unique() 
uniques 

obj.value_counts()

obj

# isin checks each element if series elements is in the sequence
mask = obj.isin(["b", "c"])
mask 
obj[mask]

# Index.get_indexer gives you an index array from an array of possibly nondistinct values into another array of distinct values
# it converts them into the position of unique_vals with that value
to_match = pd.Series(["c", "a", "b", "b", "c", "a"])
unique_vals = pd.Series(["c", "b", "a"])
indices = pd.Index(unique_vals).get_indexer(to_match)
indices 

# unique, value counts, and set membership methods
# isin - yields boolean array if each series/df value is contained in the sequence
# get_indexer - computes integer indices for each value in an array into another array of distinct values
# unique - computes array of unique values in a series
# value_counts