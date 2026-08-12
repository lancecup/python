import pandas as pd 
import numpy as np 

# ============================================================================ #
#                             Handling Missing Data                            #
# ============================================================================ #

# we get NaNs for missing data
# .isna() method returns boolean series 
float_data = pd.Series([6, 7, np.nan, 0])
float_data.isna()

# None is also NA
string_data = pd.Series(["aardvark", np.nan, None, "avocado"])
string_data 
string_data.isna()
float_data = pd.Series([1, 2, None], dtype='float64')
float_data.isna()

# NA handling methods
# dropna - filter axis labels based on whether values for each label have missing data
# fillna - fill in with some value or interpolation method like ffill or bfill
# isna - check which values are na
# notna - isna but reverse

# ------------------------- Fitering Out Missing Data ------------------------ #
# can filter using isna, but dropna also works
data = pd.Series([1, np.nan, 3.5, np.nan, 7])
data.dropna()
data[data.notna()] # equivalent 

# for data frames, there are different ways
# dropna by default removes any row with a nan

data = pd.DataFrame([[1., 6.5, 3.], 
                     [1., np.nan, np.nan], 
                     [np.nan, np.nan, np.nan], [np.nan, 6.5, 3.]])
data 
data.dropna()

# how = "all" drops only rows with all na
data.dropna(how = "all")

# to drop columns in the same way, pass axis = "columns"
data[4] = np.nan 
data.dropna(axis = "columns", how = "all")

# if you want to keep only rows with at most a certain number of missing obs, you can use thresh argument

df = pd.DataFrame(np.random.standard_normal((7, 3)))
df.iloc[:4, 1] = np.nan
df.iloc[:2, 2] = np.nan
df 
df.dropna()
df.dropna(thresh = 2) # less than 2 nans per row

# -------------------------- Filling In Missing Data ------------------------- #
# can fill in with fillna(), inputting a dictionary with colnames as keys assigns diff fill values by col

df.fillna(0)
df.fillna({1:0, 2:10})
df = pd.DataFrame(np.random.standard_normal((6, 3)))

df.iloc[2:, 1] = np.nan
df.iloc[4:, 2] = np.nan
df 

df.ffill()
df.ffill(limit = 2)
df.bfill()

data = pd.Series([1., np.nan, 3.5, np.nan, 7])
data.fillna(data.mean())

# ============================================================================ #
#                              Data Transformation                             #
# ============================================================================ #

# ---------------------------- Removing Duplicates --------------------------- #
data = pd.DataFrame({"k1": ["one", "two"] * 3 + ["two"], 
                     "k2": [1, 1, 2, 3, 3, 4, 4]})
data 

# .duplicated() returns a boolean series if each row is a duplicate
data.duplicated()

# .drop_duplicates() returns a df with rows where .duplicated is false
data.drop_duplicates()

# you can specify th any subset of cols to detect duplicates
# suppose filter duplicates only based on k1
data["v1"] = range(7)
data 
data.drop_duplicates(subset = ["k1"])

# they keep the first observe value combination
# keep = "last" will return the last one
data.drop_duplicates(["k1", "k2"], keep = "last")

# --------------- Transforming Data using a Function / Mapping --------------- #
data = pd.DataFrame({"food": ["bacon", "pulled pork", "bacon",
                              "pastrami", "corned beef", "bacon",
                              "pastrami", "honey ham", "nova lox"],
                              "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
data 

# suppose you want to add a column indicating the type of animal each food came from

meat_to_animal = {
  "bacon": "pig",
  "pulled pork": "pig",
  "pastrami": "cow",
  "corned beef": "cow",
  "honey ham": "pig",
  "nova lox": "salmon"
}

data["animal"] = data["food"].map(meat_to_animal)
# map assigns key from food to assign value for animal

# we could also pass a function
def get_animal(x):
    return meat_to_animal[x]
data["food"].map(get_animal)

# map is convenient way to perform element-wise transformations

# ----------------------------- Replacing Values ----------------------------- #

# replace provides a simpler way to replace values
data = pd.Series([1., -999., 2., -999., -1000., 3.])
data 

data.replace(-999, np.nan) # replacing -999 with nan
data.replace([-1000, -999], np.nan) # replacing multiple values via list
data.replace({-999 : np.nan, -1000 : 0})

# --------------------------- Renaming Axis Indexes -------------------------- #

data = pd.DataFrame(np.arange(12).reshape((3, 4)), 
                    index=["Ohio", "Colorado", "New York"], 
                    columns=["one", "two", "three", "four"])

def transform(x):
    return x[:4].upper()

data.index.map(transform)


# you can assign to the index attribute - modifying the df
data.index = data.index.map(transform)
data 

# if you want to create a transformed version of a dataset without modifying the original, use rename
data.rename(index = str.title, columns = str.upper)
# does not modify the original

# rename can be used with a dictionary-like object 
data.rename(index = {"OHIO" : "INDIANA"},
            columns = {"three" : "peekaboo"})

# ------------------------ Discretization and Binning ------------------------ #
# continuous data is discretized into bins

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]

age_categories = pd.cut(ages, bins)
age_categories 

age_categories.codes # each bin is identified by a special interval value
age_categories.categories # the bin they belong to
age_categories.categories[0] # the bin of the first
age_categories.value_counts()

# you can change which side is closed by passing right = False
pd.cut(ages, bins, right = False)

# you can override the default interval-baed bin labeling by passing a list to the labels
group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]
pd.cut(ages, bins, labels = group_names)

# if you pass an integer number of bins rather than bin edges
# it will compute equal lenght bins
data = np.random.uniform(size = 20)
pd.cut(data, 4, precision = 2) # precision limits the decimal precision to two digits

# very similarly, pd.qcut bins the data based on sample quantiles
data = np.random.standard_normal(1_000)
quartiles = pd.qcut(data, 4, precision = 2)
quartiles 
quartiles.value_counts()

# you can pass your own quantiles (numbers between 0 and 1)
pd.qcut(data, [0, 0.1, 0.5, 0.9, 1]).value_counts()

# --------------------- Detecting and Filtering Outliers --------------------- #
data = pd.DataFrame(np.random.standard_normal((1000, 4)))
data.describe()

# to find values exceeding 3 in absolute value
col = data[3]
col[col.abs() > 3]

# to select the rows, you can use the any method on boolean df 
data[(data.abs() > 3).any(axis = "columns")] # checking if any of the columns have > 3

# values can be set based on this criteria
data[(data.abs() > 3).any(axis = "columns")] = np.sign(data) * 3
data.describe()

np.sign(data).head()
# np.sign(data) produces 1 and -1 based on whether pos or negative

# ---------------------- Permutation and Random Sampling --------------------- #
df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))
df 

sampler = np.random.permutation(5)
sampler

# permutation with the length of the axis you want to permute produces an array of integers indicating the new ordering
# that array can then be used in iloc or take function
df.take(sampler)
df.iloc[sampler]

# by involving with axis = "columns", can select permutation of cols
column_sampler = np.random.permutation(7)
column_sampler 
df.take(column_sampler, axis = "columns")

# to select a random subset without replacement, you can use sample method
df.sample(n = 3)
# to generate sample with replacement, pass replace = True
choices = pd.Series([5, 7, -1, 6, 4])
choices.sample(n = 10, replace = True)

# ------------------- Computing Indicator / Dummy Variables ------------------ #
# pd.get_dummies

df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
                   "data1": range(6)})
df 
pd.get_dummies(df["key"], dtype = float)

# in some cases, you may want to add a prefix to the cols in the df which can be merged with the other data
dummies = pd.get_dummies(df["key"], prefix = "key", dtype = float)
df_with_dummy = df[["data1"]].join(dummies)
df_with_dummy

# if a row belongs to multiple categories
mnames = ["movie_id", "title", "genres"]

movies = pd.read_table("datasets/movielens/movies.dat",
                       sep = "::",
                       header = None, names = mnames,
                       engine = "python")
movies[:10]

# pandas has a special series method that handles scenario of multiple group membership
dummies = movies["genres"].str.get_dummies("|")
dummies.iloc[:10, :6]

movies_windic = movies.join(dummies.add_prefix("Genre_"))
movies_windic.iloc[0]


# for much larger data, this is generally slow, it would be better to write a lower-level function
# that writes directly to a numpy array and then wrap the result in a df

# It is useful to combine get_dummies() with a discretization function like pandas.cut
np.random.seed(12345)
values = np.random.uniform(size = 10)
values 

bins = np.arange(0, 1.2, 0.2)
pd.get_dummies(pd.cut(values, bins))

# ============================================================================ #
#                              String Manipulation                             #
# ============================================================================ #

# ------------------- Python Built-In String Object Methods ------------------ #

val = "a,b,    guido"
val.split(",") # can break string into pieces with split

# split is often combined with strip to trim whitespace
pieces = [x.strip() for x in val.split(",")]
pieces 

# these substrings can be concatenated with addition
first, second, third = pieces 
first + "::" + second + "::" + third 

# A faster way is to pass a list or tuple to the join method on the string "::"
"::".join(pieces)

# Other methods are concerned with locating substrings
# using python's in keyword is the best way to detect a substring though index and find can also be used
"guido" in val 
val.index(",")
val.find(":")
# find raises an exception if the string isn't found, while index raises an exception where find returns -1

val.index(":")

val.count(",") # number of , in the string
val.replace(",", "::") # replace , with ::
val.replace(",", "")

# Python built-in string methods
# count - number of occurrences of substring in the string
# endswith - if string ends with the suffix
# startswith - if string starts with the prefix
# join - use string as delimiter for concatenating a sequence of other strings - joins together strings
# index - return starting index of the first occurence of passed substring if found in the string
# find - return position of first character of first occurrence of substring in the string (-1 if not found)
# rfind - " last character
# replace - replaces occurences of string with another string
# strip, rstrip, lstrip - trim whitespace 
# split - break string into list of substrings using passed delimiter
# lower - convert alphabet characters to lowercase
# upper - convert alphabet characters to uppercase
# ljust, rjust - left justify or right justify

# ---------------------------- Regular Expressions --------------------------- #
# language for describing text patterns

# r"cat" matches cat 

# regex symbols
# . - any character except usually newline
# \d - digit
"these are a single character"
"\d+ is for multiple digits"

import re
re.findall(r"\d+", "I have 12 apples and 300 oranges") # ['12', '300']

# \D - not a digit
# \w - word character: letters, digits, _
"letters, digits, underscore"
re.findall(r"\w+", "hello world_123!") # ['hello', 'world_123']

# \W - not a word character
# \s - whitespace
"space, tab, newline"
text = "foo    bar\t baz  \tqux"
re.split(r"\s+", text) # ['foo', 'bar', 'baz', 'qux']


# \S - not whitespace
# [...] - one character from a set
"match one character from this collection"
r"[abc]" # matches a, b, c
re.findall(r"[abc]", "apple banana") # finds every a, b, or c

"ranges work too"
r"[A-Z]"
r"[a-z]"
r"[0-9]"
r"[A-Za-z0-9]" # combining all 3

re.findall(r"[^0-9]+", "abc123xyz456")

# [^...] - one character not in the set


#! QUANTIFIERS
# * - 0 or more
"0 or more of the preceding character"

r"a*" # "", "a", "aa", "aaa"

# + - 1 or more
r"a+" # a, "aa", "aaa", ...

# ? - 0 or 1
r"colou?r" # matches both colour or color

# {n} - exactly n
r"\d{4}" # means exactly 4 digits

# {n,m} - between n and m
r"\d{2,4}" # between 2 and 4 digits

# {n,} - at least n 
r"\d{3,}" # 3 or more digits


#! ANCHORS - positions
# ^ - start of string
r"^Hello" # matches Hello there, not Say Hello

# $ - end of string
r"com$" # matches google.com, not google.com.au

### regex methods
# search() is this pattern anywhere in the string

text = "My phone number is 555-1234"

m = re.search(r"\d+", text)
m.group()# matched text

# positions 
m.start()
m.end()
m.span()

# match() - only checks the beginning
re.match(r"\d+", "123abc") # match
re.match(r"\d+", "abc123") # not match
# search - anywhere, match - beginning

# re.fullmatch() # does the entire string match this pattern
re.fullmatch(r"\d{5}", "12345") # matches
re.fullmatch(r"\d{5}", "abc12345") # no match

# re.findall() - returns all matching pieces
text = "There are 12 cats, 8 dogs, and 400 birds."
re.findall(r"\d+", text)

# re.finditer() - returns match objects
for match in re.finditer(r"\d+", text):
    print(match.group(), match.span())
# use this when you need both the matched value and its location

# re.split() - can define where you want to split
re.split(r"\s+", text) # can split on any amount of whitespace
text = "apple,banana;orange grape"
re.split(r"[,;\s]+", text)
# r"[,;\s]+" means one or more commas, semicolons, or whitespace chars

# re.sub() - means substitute
text = "My number is 5551234567"

re.sub(r"\d", "X", text)
# you can replae whole sequences
re.sub(r"\d+", "NUMBER", "I have 12 cats and 4 dogs")
# re.sub(pattern, replacement, text)

# () - parentheses let you capture pieces of a match
email = "dave@google.com"
r"(\w+)@(\w+)\.(\w+)"
# three groups (\w+) username \\ (\w+) domain \\ (\w+) suffix

m = re.match(r"(\w+)@(\w+)\.(\w+)", email)
m.group()
m.group(1)

# Named groups
pattern = r"(?P<username>\w+)@(?P<domain>\w+)\.(?P<suffix>\w+)"
m = re.match(pattern, "dave@google.com")
m.group("username")

# OR | 
r"cat|dog"
re.findall(r"cat|dog", "I have a cat and a dog")
r"(cat|dog)s" # cat(s) or dog(s)

# Word boundaries \b 

# if you want cat specifically
r"\bcat\b"
# since r"cat" would match category, scatter, etc. 

### Regex is built piece by piece
r"[A-Z0-9._%+-]+@[A-Z0-9._%+-]+\.[A-Z]{2,4}"

### Flags
# re.IGNORECASE 
re.findall(r"cat", "Cat CAT cat", flags = re.IGNORECASE)
# re.MULTILINE - changes how ^ and $ behave for multiline text

### Compiling regex 

# instead of 
# re.findall(r"\d+", text1)
# re.findall(r"\d+", text2)
# re.findall(r"\d+", text3)

# you can compile once then findall thrice
# regex = re.compile(r"\d+)
# regex.findall(text1) 
# regex.findall(text2)
# regex.findall(text3)

email_pattern = re.compile(
    r"[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}",
    flags = re.IGNORECASE
)

### Common practical patterns
r"\d+" # digits
r"\w+" # words
r"\s+" # whitespaces
r"^\d{5}" # exactly 5 digits
r"[+-]?\d+" # optional sign
r"[+-]?\d+(?:\.\d+)?" # decimal number
r"\d{4}-\d{2}-\d{2}" # date like yyyy-mm-dd
r"\d{3}-\d{3}-\d{4}" # phone number
r"\ba\w*" # words beginning with a

### regex + pandas
df["name"].str.contains(r"^A") # find rows where the name starts with A
df["phone"].str.replace(r"\D", "", regex = True) # replace patterns (anything not a digit remove it)
df["text"].str.split(r"\s+") # split using regex

### contains, match, fullmatch, extract
# s.str.contains(pattern) # does the pattern occur anywhere
# s.str.match(pattern) # does the beginning match
# s.str.fullmatch(pattern) # does the whole string match
# s.str.extract(pattern) # give the captured parts

# ------------------------ String Functions in pandas ------------------------ #
data = {"Dave": "dave@google.com", "Steve": "steve@gmail.com",
        "Rob": "rob@gmail.com", "Wes": np.nan}
data = pd.Series(data)
data 
data.isna()

data.str.contains("gmail")

pattern = r"([A-Z0-9._%+-]+@([A-Z0-9.-]+)\.([A-Z]{2,4}))"
data.str.findall(pattern, flags = re.IGNORECASE)

matches = data.str.findall(pattern, flags = re.IGNORECASE).str[0]
matches
matches.str.get(1)

# you can similarly slice strings 
data.str[:5]

# str.extract will return the captured groups of a regex as a df
data.str.extract(pattern, flags = re.IGNORECASE)

### Series string methods
# cat - concatenate strings element wise 
# contains - returns boolean array if string contains pattern
# count - count occurrences of pattern
# extract - use regex with groups to extract one or more strings from a series of strings
# endswith -
# startswith - 
# findall - compute list of all occurences of pattern/regex for each string
# get - index into each element (retrieve ith element)
# isalnum - is alpha numeric
# isalpha - is alphabetical
# isdecimal - 
# isdigit 
# islower - lower case
# isnumeric 
# isupper 
# join - join strings together with separator  -- sep.join(list_of_strings)
# len - compute length of each string
# lower, upper - convert cases
# match - T or F whether it matches
# pad - add white space
# center - pad both sides
# repeat - duplicate values -- s.str.repeat(3) is equiv x * 3 
# replace - replace pattern with string
# slice - slice each string in the series
# split - split strings 
# strip, rstrip, lstrip - trim whitespace

# ============================================================================ #
#                               Categorical Data                               #
# ============================================================================ #

values = pd.Series(['apple', 'orange', 'apple', 'apple'] * 2)
values 
pd.unique(values) 
values.value_counts()

values = pd.Series([0, 1, 0, 0] * 2)
dim = pd.Series(["apple", "orange"])
values 
dim 

# we can use the take method to restore the original series
dim.take(values)

# ------------------- Categorical Extension Type in pandas ------------------- #
# pandas has a special categorical extension 

fruits = ["apple", "orange", "apple", "apple"] * 2
N = len(fruits)
rng = np.random.default_rng(seed = 12345)
df = pd.DataFrame({'fruit': fruits, 
                   'basket_id': np.arange(N),
                   'count': rng.integers(3, 15, size=N),
                   'weight': rng.uniform(0, 4, size=N)},
                   columns=['basket_id', 'fruit', 'count', 'weight'])
df 

# here df["fruit"] is an array of python string objects
# we can convert it to catorical by astype("category")
fruit_cat = df["fruit"].astype("category")
fruit_cat 

# you can access the values 
c = fruit_cat.array 
type(c)

# categories and codes attributes
c.categories 
c.codes 

# can get a mapping between codes and categories
dict(enumerate(c.categories)) 

# you can convert a df col to categorical by assigning th econverted result
df["fruit"] = df["fruit"].astype("category")
df["fruit"]

# you can create pd.Categorical directly from other types of python sequences
my_categories = pd.Categorical(["foo", "bar", "baz", "foo", "bar"])
my_categories 

# if you have obtained categorical encoded data from another source, you can use from_codes constructor
categories = ["foo", "bar", "baz"]
codes = [0, 1, 2, 0, 0, 1]
my_cats_2 = pd.Categorical.from_codes(codes, categories)
my_cats_2 

# categories array may be in a different order depending on input data
# when using from_codes, can indicate meaningful ordering
ordered_cat = pd.Categorical.from_codes(codes, categories, ordered = True)
ordered_cat 

# an unordered categorical instance can be made ordered with as_ordered()
my_cats_2.as_ordered()

# ---------------------- Computations with Categoricals ---------------------- #
# some parts of pandas perform better with categoricals (some functions can use the ordered flag)

# consider some random numeric data and use the qcut bin functions
rng = np.random.default_rng(seed = 12345)
draws = rng.standard_normal(1_000)
draws[:5]

# let's compute a quartile binning of this data and extract some stats
bins = pd.qcut(draws, 4)
bins 

# the exact sample quartiles may be less useful than quartile names
# we add labels to qcut
bins = pd.qcut(draws, 4, labels = ["Q1", "Q2", "Q3", "Q4"])
bins 
bins.codes[:10]

# the bins categoriacl does not contain info on the bin edges in teh data
# we can use groupby to extract some summary stats
bins = pd.Series(bins, name = "quartile")
results = (pd.Series(draws)
            .groupby(bins)
            .agg(["count", "min", "max"])
            .reset_index())
results 
# quartile col retains original categorical info including ordering from bins
results["quartile"]


## Better performance

N = 10_000_000

labels = pd.Series(['foo', 'bar', 'baz', 'qux'] * (N // 4))

# convert labels to categorical
categories = labels.astype("category")

# compare memory usage 
labels.memory_usage(deep = True)
categories.memory_usage(deep = True)

# groupby operations can be significantly faster with categoricals since the algorithms use integer-based codes instead of strings

# ---------------------------- Categorical methods --------------------------- #
s = pd.Series(['a', 'b', 'c', 'd'] * 2)

cat_s = s.astype('category')
cat_s

# the special accessor attribute is cat
cat_s.cat.codes 
cat_s.cat.categories

# if we know the actual categories are beyond the ones here, 
# we can set_categories
actual_categories = ["a", "b", "c", "d", "e"]
cat_s2 = cat_s.cat.set_categories(actual_categories)
cat_s2 

# in large datasets, categoricals are often used for memory savings and better performance
# after you filter, many of the categories may not appear in the data
# we can use the remove_unused_categories to trim unobserved categories
cat_s3 = cat_s[cat_s.isin(["a", "b"])]
cat_s3 
cat_s3.cat.remove_unused_categories()

### Categorical methods
# add_categories - append them
# as_ordered 
# as_unordered
# remove_categories
# remove_unused_categories 
# rename categories
# reorder_categories
# set_categories

# ------------------- Creating dummy variables for modeling ------------------ #
# you'll often transform categorical data into dummies
cat_s = pd.Series(['a', 'b', 'c', 'd'] * 2, dtype='category')

# use the get_dummies function
pd.get_dummies(cat_s, dtype = float)
