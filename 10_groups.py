import numpy as np 
import pandas as pd 

# ============================================================================ #
#                        Thinking about Group Operations                       #
# ============================================================================ #
df = pd.DataFrame({"key1" : ["a", "a", None, "b", "b", "a", None],
                    "key2" : pd.Series([1, 2, 1, 2, 1, None, 1],
                                       dtype="Int64"),
                    "data1" : np.random.standard_normal(7),
                    "data2" : np.random.standard_normal(7)})

df 

# if you want to compute the mean of the data1 col based on key
grouped = df["data1"].groupby(df["key1"])
grouped # groupby object 
# hasn't computed anything but only does it when we call a method

grouped.mean()

# if we instead passed multiple arrays as a list
means = df["data1"].groupby([df["key1"], df["key2"]]).mean()
means 
# we grouped the data using two keys and the resulting series has a hierarchical index
means.unstack()

# group keys can be arrays of the right length
states = np.array(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
years = [2005, 2005, 2006, 2005, 2006, 2005, 2006]

df["data1"].groupby([states, years]).mean()

# if the group keys are cols in the same df, just use colname
df.groupby("key1").mean()

df.groupby("key2").mean(numeric_only = True)

df.groupby(["key1", "key2"]).mean()

# generally useful to call size method to show group sizes
df.groupby(["key1", "key2"]).size()

# any missing values in a group key are excluded from the result by default
# this can be disabled by passing dropna = False 
df.groupby("key1", dropna = False).mean()

# can also use count() instead of size to get number of nonnull values in each group
df.groupby("key1").count()
df.groupby("key1").size()

# --------------------------- Iterating over Groups -------------------------- #
# groupby supports iteration as it generates a sequence of 2-tuples containing groupname and chunk of data

for name, group in df.groupby("key1"):
    print(name)
    print(group)

# for multiple keys, the first element is a tuple of the keys
for (k1, k2), group in df.groupby(["key1", "key2"]):
    print((k1, k2))
    print(group)

# it could be useful to compute a dictionary of the data pieces as a one-liner
pieces = {name: group for name, group in df.groupby("key1")}
pieces["b"]

# ------------------ Selecting a Column or Subset of Columns ----------------- #
# indexing a groupby object created from a df with a colname has the effect of column subsetting for aggregation
df.groupby("key1")["data1"]  # essentially df["data1"].groupby(df["key1"])
df.groupby("key1")[["data2"]] # df[["data2"]].groupby(df["key2"])

# it may be desirable to aggregate only a few columns
# to compute means for just the data2 col and get the result as a df:
df.groupby(["key1", "key2"])[["data2"]].mean() # returns a df
df.groupby(["key1", "key2"])["data2"].mean() # returns a series

# the object returned by indexing is a grouped df if a list is passed
# a grouped series is returned if only a single col is passed
s_grouped = df.groupby(["key1", "key2"])["data2"]
s_grouped 
s_grouped.mean