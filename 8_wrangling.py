import pandas as pd 
import numpy as np 

# ============================================================================ #
#                             Hierarchical Indexing                            #
# ============================================================================ #

# two or more index levels on an axis

data = pd.Series(np.random.uniform(size=9),
                 index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"],
                        [1, 2, 3, 1, 3, 1, 2, 2, 3]])

data.index 

# partial indexing lets you select subsets of the data
data["b"]
data["b":"c"]
data.loc[["b", "d"]]

# can select from an inner level, e.g. selecting all htat have 2 from the second index level
data[:, 2]

# you can rearrange this data into a df using unstack()
data.unstack()
data.unstack().stack() # undo 

# either axis in a df can have a hierarchical index
frame = pd.DataFrame(np.arange(12).reshape((4, 3)),
                      index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
                      columns=[["Ohio", "Ohio", "Colorado"],
                               ["Green", "Red", "Green"]])
frame 

# hierarchical levels can have names, if they do, it will show in the console output
frame.index.names 
frame.index.names = ["key1", "key2"]
frame.columns.names = ["states", "color"]
frame 

# nlevels attribute shows how many levels an index has
frame.index.nlevels
frame.columns.nlevels

# partial column indexing lets you select groups of columns
frame["Ohio"]

# a multiindex can be created by itself and then reused
pd.MultiIndex.from_arrays([["Ohio", "Ohio", "Colorado"],
                           ["Green", "Red", "Green"]],
                           names = ["state", "color"])

# ----------------------- Reordering and Sorting Levels ---------------------- #
# swapping index levels for rows
frame.swaplevel("key1", "key2")

# sort the rows based on the row index
# level 0 is the leftmost key, then level 1 is key2
frame 
frame.sort_index(level = 1) # note
frame.sort_index(level = 0)
frame.swaplevel(0, 1).sort_index(level = 0)

# data selection is much better on hierarchically indexed objects if teh index is 
# lexicographically sorted using the outermost level
# i.e. sort_index(level = 0)

# ------------------------ Summary Statistics by Level ----------------------- #
# we can aggregate by key2 with groupby
frame.groupby(level = "key2").sum()
frame.groupby(level = "color", axis = "columns")

# ----------------------- Indexing with a df's Columns ----------------------- #
# may want to make col -> row index and vice versa

frame = pd.DataFrame({"a": range(7), "b": range(7, 0, -1),
                      "c": ["one", "one", "one", "two", "two",
                            "two", "two"],
                      "d": [0, 1, 2, 0, 1, 2, 3]})
frame 

# set_index creates df using cols as the index
frame2 = frame.set_index(["c", "d"])
frame2 

# by default, the cols are removed from the df, they can be kept with drop = False
frame.set_index(["c", "d"], drop = False)

# reset_index moves the index levels into the cols
frame2.reset_index()

# ============================================================================ #
#                        Combining and Merging Datasets                        #
# ============================================================================ #

# data can be combined with the functions
# pd.merge - connect rows in dfs based on one or more keys
# pd.concat - stack objects together along an axis
# combine_first - splice together overlapping data to fill in missing values in one object with values from another

# ---------------------- Database-Style DataFrame Joins ---------------------- #
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"],
                    "data1": pd.Series(range(7), dtype="Int64")})
df2 = pd.DataFrame({"key": ["a", "b", "d"],
                    "data2": pd.Series(range(3), dtype="Int64")})
df1 
df2 

merged = pd.merge(df1, df2) # many to one join
pd.merge(df1, df2, on = "key")

# if the column names are different in each object, you can specify them separately
df3 = pd.DataFrame({"lkey": ["b", "b", "a", "c", "a", "a", "b"],
                    "data1": pd.Series(range(7), dtype="Int64")})
df4 = pd.DataFrame({"rkey": ["a", "b", "d"],
                    "data2": pd.Series(range(3), dtype="Int64")})

pd.merge(df3, df4, left_on = "lkey", right_on = "rkey")

# note that c and d are missing 
# by default, merge does an inner join
# other options are left, right, and outer
# outer join takes the union of the keys, combining both left and right
pd.merge(df1, df2, how = "outer")
pd.merge(df3, df4, left_on = "lkey", right_on = "rkey", how = "outer")

## m-m merges formt he cartesian product of the matching keys
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
                    "data1": pd.Series(range(6), dtype="Int64")})
df2 = pd.DataFrame({"key": ["a", "b", "a", "b", "d"],
                    "data2": pd.Series(range(5), dtype="Int64")})
df1 
df2 
pd.merge(df1, df2, on = "key", how = "left")

# to merge with multiple keys, pass a list in the on = option
left = pd.DataFrame({"key1": ["foo", "foo", "bar"],
                     "key2": ["one", "two", "one"],
                     "lval": pd.Series([1, 2, 3], dtype='Int64')})

right = pd.DataFrame({"key1": ["foo", "foo", "bar", "bar"],
                      "key2": ["one", "one", "one", "two"],
                      "rval": pd.Series([4, 5, 6, 7], dtype='Int64')})

pd.merge(left, right, on = ["key1", "key2"], how = "outer")

# the indexes of the df objects are discarded when merging so you can reset_index
# then you set_index the cols after the merge to put it back

# when you have overlapping cols, it will append _x _y 
pd.merge(left, right, on = "key1")

# you could rename manually, or you can set the suffixes option to specify the strings to append
pd.merge(left, right, on = "key1", how = "left", suffixes = ("_left", "_right"))

## pd.merge function arguments
# pd.merge(left, right, ...)
# left - df on the left side
# right - df on the right side
# how - type of join - inner, outer, left, right
# on - the key to join by
# left_on - key on the left if different key names
# right_on - 
# left_index - if the row index in left df is the join key
# right_index 
# sort - sort merged data by join keys - False by default
# suffixes - set of strings for suffixes
# validate - verifies if the merge is of the specified type
# indicator - adds _merge with left_only, right_only, or both

# ----------------------------- Merging on Index ----------------------------- #

left1 = pd.DataFrame({"key": ["a", "b", "a", "a", "b", "c"],
                      "value": pd.Series(range(6), dtype="Int64")})
right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])

left1 
right1 

pd.merge(left1, right1, left_on = "key", right_index = True)

# notice that the index for left1 has been preserved
# this is because the index of right1 is unique
# this m-1 merge can perserve the index values from left1 that correspond to rows in the output

# you can get the union of the keys with outer
pd.merge(left1, right1, left_on = "key", right_index = True, how = "outer")

# hierarchically indexed data is more complicated since joinin on index is multi-key merge
lefth = pd.DataFrame({"key1": ["Ohio", "Ohio", "Ohio",
                                "Nevada", "Nevada"],
                       "key2": [2000, 2001, 2002, 2001, 2002],
                       "data": pd.Series(range(5), dtype="Int64")})

righth_index = pd.MultiIndex.from_arrays(
     [
         ["Nevada", "Nevada", "Ohio", "Ohio", "Ohio", "Ohio"],
         [2001, 2000, 2000, 2000, 2001, 2002]
     ]
)
righth = pd.DataFrame({"event1": pd.Series([0, 2, 4, 6, 8, 10], dtype="Int64",
                                            index=righth_index),
                        "event2": pd.Series([1, 3, 5, 7, 9, 11], dtype="Int64",
                                            index=righth_index)})

lefth 
righth 

# here you have to indicate multiple cols to merge on as a list
pd.merge(lefth, righth, left_on = ["key1", "key2"], right_index = True, how = "outer")

# can also use both indexes

left2 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]],
                     index=["a", "c", "e"],
                     columns=["Ohio", "Nevada"]).astype("Int64")

right2 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]],
                      index=["b", "c", "d", "e"],
                      columns=["Missouri", "Alabama"]).astype("Int64")

pd.merge(left2, right2, left_index = True, right_index = True, how = "outer")

## Can also use .join method on data to left join similarly

left2.join(right2) # default is left but can specify how as above
left2.join(right2, how = "outer")
left1.join(right1, on = "key")

#for simple index-index merges, you can pass a list of dfs to join as an alternative
another = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]],
                       index=["a", "c", "e", "f"],
                       columns=["New York", "Oregon"])
left2.join([right2, another])
left2.join([right2, another], how = "outer")

# ------------------------ Concatenating along an Axis ----------------------- #
arr = np.arange(12).reshape((3, 4))
arr 
np.concatenate([arr, arr], axis = 1) 

# you have additional concerns with dfs
# if the objects are indexed differently on other axes, should we combine distinct elements or keep common only
# do the concatenated chunks of data need to be identifiable
# does the concatenation axis contain data that needs to be preserved

s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")

s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")

s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")

s1 
s2 
s3 
pd.concat([s1, s2, s3]) # default is it appends at the bottom of df, along axis = "index"
pd.concat([s1, s2, s3], axis = "columns")
s4 = pd.concat([s1, s3])
s4 

pd.concat([s1, s4], axis = "columns")
pd.concat([s1, s4], axis = "columns", join = "inner")

# suppose you wanted to create a hierarchical index on the concatenation index, use the keys arg
result = pd.concat([s1, s1, s3], keys=["one", "two", "three"])
result 
result.unstack()

# when combining series along axis = "columns", keys become the df colnames
pd.concat([s1, s2, s3], axis="columns", keys=["one", "two", "three"])


df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=["a", "b", "c"],
                    columns=["one", "two"])
df2 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=["a", "c"],
                    columns=["three", "four"])
df1 
df2 
pd.concat([df1, df2], axis = "columns", keys = ["lvl1", "lvl2"])

# if you pass a dictionary, the dictionary's keys will be the keys option
pd.concat({"lvl1": df1, "lvl2": df2}, axis = "columns")

# if there's no row index, ignore_index = true
df1 = pd.DataFrame(np.random.standard_normal((3, 4)),
                    columns=["a", "b", "c", "d"])
df2 = pd.DataFrame(np.random.standard_normal((2, 3)),
                    columns=["b", "d", "a"])
df1 
df2 
pd.concat([df1, df2], ignore_index = True)

## pd.concat(objs, ...) args
# objs - list or dictionary of objects to concatenate
# axis - axis to concatenate along 
# join - inner or outer - whether to intersect or union indexes
# keys - identifiers of which data belongs to which df originally pre-concat
# levels - indexes to use as hierarchical index level or levels if keys passed
# names - names for created hierarchical levels if keys / levels passed
# verify_integrity - check new axis for duplicates and raise exception if so
# ignore_index - for when there's no index

# ------------------------ Combining Data with Overlap ----------------------- #
# a.combine_first(b) method checks if a is na, then if so, put b if not keep a

df1 = pd.DataFrame({"a": [1., np.nan, 5., np.nan],
                    "b": [np.nan, 2., np.nan, 6.],
                    "c": range(2, 18, 4)})

df2 = pd.DataFrame({"a": [5., 4., np.nan, 3., 7.],
                    "b": [np.nan, 3., 4., 6., 8.]})
df1 
df2 
df1.combine_first(df2)

# ============================================================================ #
#                            Reshaping and Pivoting                            #
# ============================================================================ #

# ------------------- Reshaping with Hierarchical Indexing ------------------- #
# two primary actions, 
# stack - this rotates or pivots from the columns in the data to the rows
# unstack - this pivots from the rows into the columns

# stack: wide -> long
# unstack: long -> wide

# e.g. wide
#        math  english  science
# Alice    90       85       92
# Bob      78       88       81

# e.g. long 
# Alice  math       90
# Alice  english    85
# Alice  science    92
# Bob    math       78
# Bob    english    88
# Bob    science    81

data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(["Ohio", "Colorado"], name="state"),
                    columns=pd.Index(["one", "two", "three"],
                    name="number"))
data 

# stack pivots the cols into rows yielding a series
result = data.stack()
result
result.unstack()

# by default, the innermost level is unstacked
# you can unstack a different level by passing a level number or name
result.unstack(level = 0)
result.unstack(level = "state")

# unstacking might introduce nans if all of the values in the level aren't found in each subgroup
s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")

s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")

data2 = pd.concat([s1, s2], keys=["one", "two"])
data2 

data2.unstack()
data2.unstack().stack()
data2.unstack().stack().dropna()

# when you unstack, the level unstacked becomes the lowest level in the result
df = pd.DataFrame({"left": result, "right": result + 5},
                  columns=pd.Index(["left", "right"], name="side"))
df
df.unstack(level = "state")

# we can indicate the name to stack also
df.unstack(level = "state").stack(level = "side")

# --------------------------- Pivoting Long to Wide -------------------------- #
data = pd.read_csv("examples/macrodata.csv")
data = data.loc[:, ["year", "quarter", "realgdp", "infl", "unemp"]]
data.head()

# use pd.PeriodIndex - represents time intervals to combine year and quarter
periods = pd.PeriodIndex.from_fields(
    year=data.pop("year"),
    quarter=data.pop("quarter"),
).rename("date")
# .pop removes the col from original df and outputs just the col

data.index = periods.to_timestamp("D")
data.head()

# then select subset of cols and give th ecols index the name item
data = data.reindex(columns = ["realgdp", "infl", "unemp"])
data.columns.name = "item"
data.head()

# finally, reshape with stack
long_data = data.stack().reset_index().rename(columns = {0: "value"})
long_data

# if you want a df containing one col per distinct item indexed by timestamps in date
# use pivot method
pivoted = long_data.pivot(index = "date", columns = "item",
                          values = "value")
pivoted 

# if you had two value cols to reshape simultaneously, 
# by omitting the values arg you get a df with hierarchical cols
long_data["value2"] = np.random.standard_normal(len(long_data))
long_data[:10]

pivoted = long_data.pivot(index = "date", columns = "item")
pivoted 

# note that pivot is equivalent to creating a hierarchical index using set_index followed by unstack
unstacked = long_data.set_index(["date", "item"]).unstack(level = "item")
unstacked 

# --------------------------- Pivoting Wide to Long -------------------------- #
# inverse of pivot is pd.melt
# it merges multiple cols into one producing a df longer than the input

df = pd.DataFrame({"key": ["foo", "bar", "baz"],
                    "A": [1, 2, 3],
                    "B": [4, 5, 6],
                    "C": [7, 8, 9]})
df 

# the key col can be a group indicator and the other cols are data values
# we must indicate which are the group indicators
melted = pd.melt(df, id_vars = "key")
melted 

# we can reshape back to original
reshaped = melted.pivot(index = "key", columns = "variable", values = "value")
# note that pivot makes the key the row index

# you can also specify subset of cols rto use as value columns
pd.melt(df, id_vars = "key", value_vars = ["A", "C"])

# melt can also be used without group identifiers
pd.melt(df, value_vars = ["A", "B"])