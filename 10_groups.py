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

# ------------------- Grouping with Dictionaries and Series ------------------ #
people = pd.DataFrame(np.random.standard_normal((5, 5)),
                      columns=["a", "b", "c", "d", "e"],
                      index=["Joe", "Steve", "Wanda", "Jill", "Trey"])

people
people .iloc[2:3,[1,2]] = np.nan 
people 

# suppose have a group correspondence for the cols and want to sum the cols by group
mapping = {"a": "red", "b": "red", "c": "blue", 
           "d": "blue", "e": "red", "f": "orange"}

# using this dict, we can add up the new cols
# note that f isnt used and thus not present
by_columns = people.groupby(mapping, axis = "columns")
by_columns.sum()

# this holds true for series as well
map_series = pd.Series(mapping)
map_series 

people.groupby(map_series, axis = "columns").count()

# -------------------------- Grouping with Functions ------------------------- #
# consider the previous df
# if you wanted to group by name length, you could pass the len function
people.groupby(len).sum()

# can mix arrays, dictionaries, series
key_list = ["one", "one", "one", "two", "two"]
people.groupby([len, key_list]).min()

# ------------------------- Grouping by Index Levels ------------------------- #

# can aggregate using one of th elevels of an axis index
columns = pd.MultiIndex.from_arrays([["US", "US", "US", "JP", "JP"],
                                    [1, 3, 5, 1, 3]],
                                    names=["cty", "tenor"])
hier_df = pd.DataFrame(np.random.standard_normal((4, 5)), columns = columns)
hier_df

# to group by level, pass the level number or name use the level keyword
hier_df.groupby(level = "cty", axis = "columns").count()

# ============================================================================ #
#                               Data Aggregation                               #
# ============================================================================ #

# data transformations that produces scalars from arrays
# e.g. mean, count, min, sum

# optimized groupby methods
# any, all - returns true if any or all non-NA are truthy - not 0, empty string, or false
# count - number of non-NA values
# cummin, cummax - cumulative min/max
# cumsum - cumulative sum of non-na
# cumprod - " product 
# first, last - first / last values
# mean - mean of non-na
# median - median of non-na
# min, max 
# nth - retrieve value that would appear at position n with the data in sorted
# ohlc - compute for "open-high-low-close" statistics for time series like data
# prod - product of non-na
# quantile - sample quantile
# rank - ordinal ranks of non-na
# size - compute group sizes - yields a series
# sum 
# std, var

# you can use other methods or aggregations that is defined on the object being grouped
# e.g. nsmallest works works
df 
df["data1"].groupby(df["key1"]).nsmallest(2)

# to use your own, pass it in agg
def peak_to_peak(arr):
    return arr.max() - arr.min()
grouped.agg(peak_to_peak)
grouped.describe()

# --------------- Column-wise and multiple function application -------------- #
tips = pd.read_csv("examples/tips.csv")
tips.head()
tips["tip_pct"] = tips["tip"] / tips["total_bill"]
tips.head()

# you can aggregate using a different function or multiple functions at once
grouped = tips.groupby(["day", "smoker"])
grouped_pct = grouped["tip_pct"]

grouped_pct.agg("mean")

# if you pass a list of functions, you get a df with the cols being the diff funcs
grouped_pct.agg(["mean", "max", "any", peak_to_peak])

# you can pass a tuple (name, function) so that the cols have custom names
grouped_pct.agg([("average_tip", "mean"), ("highest_tip", "max"), ("any_tip", "any"), ("difference", peak_to_peak)])


# you can also specify a list of functions to all or different funcs per col
functions = ["count", "mean", "max"]
result = grouped[["tip_pct", "total_bill"]].agg(functions) 
result 
result["tip_pct"]

ftuples = [("Average", "mean"), ("Variance", np.var)]
grouped[["tip_pct", "total_bill"]].agg(ftuples)

# to apply diff functions to diff cols, pass a dictionary to agg that maps colnames to function
grouped.agg({"tip": np.max, "size": "sum"})

grouped.agg({"tip_pct": ["min", "max", "mean", "std"], 
             "size": "sum"})

# --------------- Returning Aggregated Data without Row Indexes -------------- #

# you can disable the index by passing as_index = False in .groupby
result = tips.groupby(["day", "smoker"], as_index = False).agg({"tip_pct": ["min", "max", "mean", "std"], 
                                                       "size": "sum"})

# ============================================================================ #
#                      Apply: General split-apply-combine                      #
# ============================================================================ #
# apply splits the object being manipulated into pieces, invokes the passed function on each piece, and concatenates the pieces

# suppose you want to select top 5 tip_pct by group
def top(df, n = 5, column = "tip_pct"):
    return df.sort_values(column, ascending = False)[:n]

top(tips, n = 6)

tips.groupby("smoker").apply(top)

# functions to pass to apply must return a pandas object or scalar

# examples to solve various problems with groupby

# ------------------------ Suppressing the Group Keys ------------------------ #
# the resulting object has a hierarchical index formed from the group keys
# disable this by passing group_keys = False to groupby
tips.groupby("smoker", group_keys = False).apply(top)

# ----------------------- Quantile and Bucket Analysis ----------------------- #
# pd.cut (equal length buckets) and pd.qcut (equal size buckets)
# combine these with groupby to perform bucket or quantile analysis on data
frame = pd.DataFrame({"data1": np.random.standard_normal(1000),
                      "data2": np.random.standard_normal(1000)})

frame.head()

quartiles = pd.cut(frame["data1"], 4)
quartiles.head(10)

# the categorical object returned by cut can be passed directly into groupby
def get_stats(group):
    return pd.DataFrame(
        {"min": group.min(), "max": group.max(),
         "count": group.count(), "mean": group.mean()}
    )
grouped = frame.groupby(quartiles)
grouped.apply(get_stats).swaplevel(0, 1).sort_index(level = [0, 1])

# the same could be computed more simply with 
grouped.agg(["min", "max", "count", "mean"])

# labels = False to just get the quartile indices
quartiles_samp = pd.qcut(frame["data1"], 4, labels = False)
quartiles_samp.head()

grouped = frame.groupby(quartiles_samp)
grouped.apply(get_stats)

# ------------- Filling Missing Values with Group-Specific Values ------------ #
s = pd.Series(np.random.standard_normal(6))
s[::2] = np.nan 
s 
s.fillna(s.mean())

# if you need to fill by group, can use apply to call fillna on each chunk

states = ["Ohio", "New York", "Vermont", "Florida",
          "Oregon", "Nevada", "California", "Idaho"]

group_key = ["East", "East", "East", "East",
             "West", "West", "West", "West"]

data = pd.Series(np.random.standard_normal(8), index=states)

data
data[["Vermont", "Nevada", "Idaho"]] = np.nan 

data 

data.groupby(group_key).size()
data.groupby(group_key).count()

# fill the NA values using group means
def fill_mean(group):
    return group.fillna(group.mean())

data.groupby(group_key).apply(fill_mean)

# in another case, you might have pre-defined fill values by group
fill_values = {"East": 0.5, "West": -1}
def fill_func(group):
    return group.fillna(fill_values[group.name]) # the groups have a name attribute so we can use that

data.groupby(group_key).apply(fill_func)

# ---------------------- Random Sampling and Permutation --------------------- #
# if you wanted to draw a random sample, use sample for series

# here's how to construct a deck of card 
suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
card_val = (list(range(1, 11)) + [10] * 3) * 4
base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)

deck = pd.Series(card_val, index=cards)

# # drawing a hand of five cards-- 
def draw(deck, n = 5):
    return deck.sample(n)

draw(deck)

# two random cards from each suit
# can group based on last char and use apply
def get_suit(card):
    # last letter is suit
    return card[-1]

deck.groupby(get_suit).apply(draw, n = 2)

# we could pass group_keys = False to drop the outer suit index
deck.groupby(get_suit, group_keys = False).apply(draw, n = 2)

# ------------------ Group Weighted Average and Correlation ------------------ #
df = pd.DataFrame({"category": ["a", "a", "a", "a",
                                "b", "b", "b", "b"],
                    "data": np.random.standard_normal(8),
                    "weights": np.random.uniform(size=8)})
df 

# weighted average by category would be 
grouped = df.groupby("category")
def get_wavg(group, data_col = "data", weight_col = "weights"): 
    return np.average(group[data_col], weights = group[weight_col])
grouped.apply(get_wavg)

# stock example

close_px = pd.read_csv("examples/stock_px.csv", parse_dates=True,
                        index_col=0)

close_px.info()

close_px.tail(4)

# might want to compute a df of yearly correlations with daily returns iwth SPX
# first create a function that computes the pair-wise corrs with SPX col
def spx_corr(group):
    return group.corrwith(group["SPX"])

# then compute % change on close_px using pct_change
rets = close_px.pct_change().dropna()

# then we group these % changes by year which can be extracted from each row label
def get_year(x):
    return x.year

by_year = rets.groupby(get_year)
by_year.apply(spx_corr)

# you can also do intercolumn corrs
def corr_aapl_msft(group):
    return group["AAPL"].corr(group["MSFT"])

# ----------------------- Group-Wise Linear Regression ----------------------- #
# can use groupby to perform more complex analysis
# can regress on each chunk of data
import statsmodels.api as sm

def regress(data, yvar, xvars):
    y = data[yvar]
    X = sm.add_constant(data[xvars], has_constant = "add")
    fit = sm.OLS(y, X, missing = "drop").fit(cov_type = "HC1")

    out = {}
    for name in fit.params.index:
        out[name + "_coef"] = fit.params[name]
        out[name + "_se"] = fit.bse[name]
        out[name + "_t"] = fit.tvalues[name]
        out[name + "_p"] = fit.pvalues[name]
    out["nobs"] = fit.nobs
    out["r2"] = fit.rsquared
    return pd.Series(out)

table = by_year.apply(regress, yvar = "AAPL", xvars = ["SPX"])

# ============================================================================ #
#                   Group Transforms and "Unwrapped" groupbys                  #
# ============================================================================ #

# transform() is similar to apply()
# - it can produce a scalar value to be broadcast to the shape of the group
# - it can produce an object of the same shape as the input group 
# - it must not mutate its input

# applies a function to an array/series, keeping its shape

df = pd.DataFrame({"key": ["a", "b", "c"] * 4,
                   "value": np.arange(12.)})
df 

g = df.groupby("key")["value"]
g.mean()

# if we wanted to make a series with same dims of df["value"] but with values replaced by the average by group
def get_mean(group):
    return group.mean()

g.transform(get_mean)

def times_two(group):
    return group * 2

g.transform(times_two)

def get_ranks(group):
    return group.rank(ascending = False)

g.transform(get_ranks)

def normalize(x):
    return (x - x.mean()) / x.std()

g.transform(normalize)
g.apply(normalize)

# built-in functions like mean or sum are often much faster than a apply
g.transform("mean") 
normalized = (df["value"] - g.transform("mean")) / g.transform("std")

normalized 

# ============================================================================ #
#                                 Pivot Tables                                 #
# ============================================================================ #

# pivot reshapes long to wide

# pivot tables aggregates a table by one or more keys
# the default aggregation type is mean
tips.head()

tips.pivot_table(index = ["day", "smoker"],
                 values = ["size", "tip", "tip_pct", "total_bill"])

# this is equivalent to 
tips.groupby(["day", "smoker"])[["size", "tip", "tip_pct", "total_bill"]].mean()

# can include partial totals by passing margins = True 
# this adds an All row and column 
tips.pivot_table(index = ["time", "day"],
                 columns = "smoker",
                 values = ["tip_pct", "size"],
                 margins = True)

# to use an agg function, pass it to aggfunc 
# e.g. count 
tips.pivot_table(index = ["time", "smoker"],
                 columns = "day", 
                 values = "tip_pct", 
                 aggfunc = len,
                 margins = True)

# if some combinations are empty, you can pass a fill_value
tips.pivot_table(index = ["time", "size", "smoker"],
                 columns = "day",
                 values = "tip_pct",
                 fill_value = 0)


### pivot_table 
# values - column name or names to aggregate
# index - keys to group rows on 
# columns - column names or other group keys to group 
# aggfunc - function or list of functions to agg by
# fill_value - replace nas with 
# dropna - if True, don't include 
# margins - add row or column subtotals and grand totals
# margins_name - "All" by default
# observed - if true, only show the observed category values in the keys rather than all 

# --------------------------------- Crosstab --------------------------------- #
# special case of a pivot table that computes group frequencies 

from io import StringIO

data = """Sample  Nationality  Handedness
1   USA  Right-handed
2   Japan    Left-handed
3   USA  Right-handed
4   Japan    Right-handed
5   Japan    Left-handed
6   Japan    Right-handed
7   USA  Right-handed
8   USA  Left-handed
9   Japan    Right-handed
10  USA  Right-handed"""

data = pd.read_table(StringIO(data), sep = r"\s+")
data 

# we might want to summarize this data by nationality and handedness
pd.crosstab(data["Nationality"], data["Handedness"], margins = True)

# the first two arguments can each be array or series or list of arrays

pd.crosstab([tips["time"], tips["day"]], tips["smoker"], margins=True)