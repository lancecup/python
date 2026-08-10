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