# ============================================================================ #
#                         Data Structures and Sequences                        #
# ============================================================================ #

# ----------------------------------- Tuple ---------------------------------- #

# immutable sequences 

tup = (4, 5, 6) # can omit the parentheses
tup = 4, 5, 6

# can convert any sequence or iterator to a tuple with tuple()
tuple([4, 0, 2]) # (4, 0, 2)
tuple("string")

# elements can be accesed by index 
tup[0]

# if an object in a tuple is mutable, you can modify it in place
tup = tuple(['foo', [1, 2], True])
tup[1].append(3)
tup

# you can concatenate tuples by adding them +
# multiplying a tuple by an integer will concatenate that many copies

# you can unpack a tuple-like set of variables to unpack the tuple
tup = (4,5,6)
a, b, c = tup
b

# we commonly unpack tuples to iterate over sequences of tuples or lists
seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
for a, b, c in seq:
    print(f"a={a}, b={b}, c={c}")

# if we just want some fo the beginning elements, we can use *rest for the rest we dont care for to get a list
values = 1, 2, 3, 4, 5

# if we dont care about the rest, can use underscore instead
a, b, *_ = values 
a
b

# there aren't much methods since a tuple is immutable, a particularly useful on is count
a = (1, 2, 2, 2, 3, 4, 2)
a.count(2) # counts the number of times 2 appears in the tuple

# ----------------------------------- List ----------------------------------- #

# mutable and use [] or list() 
a_list = [2, 3, 7, None]

# semantically similar to tuples and can be used interchangeably in many functions

# list() is often used to materialize an iterable 

# add elements with .append() (at the end) and .insert(index, what_to_insert)
b_list = ["foo", "bar", "baz"]
b_list.append("dwarf")
b_list.insert(1, "red")

# the inverse of .insert() is .pop(index) 
# .remove() removes the first value from the list
b_list.append("foo")
b_list.remove("foo")

# check if a list has a value using in
"dwarf" in b_list # True

# we concatenate and combine lists similarly to tuples
# though it is computationally cheaper to use .extend()
list_of_lists = [[1, 2, 3], [4, 5], [6, 7]]
everything = []
for chunk in list_of_lists:
    everything.extend(chunk) # adds all elements of chunk to everything

everything

# you can sort a list using .sort
a = [7, 2, 5, 1, 3]
a.sort()
a 
# sort has few options that are useful
# can pass a sort key that produces a value to sort the objects
b = ["saw", "small", "He", "foxes", "six"]

b.sort(key=len)

b
['He', 'saw', 'six', 'small', 'foxes']

# list indexing
# list[start:end-1:step]

seq = [7, 2, 3, 7, 5, 6, 0, 1]

seq[1:5]
seq[3:5] = [10, 3] # can actually reassign like this
# [7,5] -> [10,3]

# negative indices slice the sequence relative to the end
seq[-4:]
seq[-6:-2]

"hello!"
# 0, 1, 2, 3, 4, 5, 6
#-6,-5,-4,-3,-2,-1

# -------------------------------- Dictionary -------------------------------- #

# stores a collection of key-value pairs 
empty_dict = {}

d1 = {"a":"some value", "b":[1,2,3,4]}
d1
d1[7] = "an integer" # adding a new pair
d1["b"]

# you can check if a dictionary contains a key like a list
"b" in d1

# you can delete values using either del or pop
d1[5] = "some value"
d1
d1["dummy"] = "another value"

del d1[5]

ret = d1.pop("dummy")
ret
d1

# keys and values method gives iterators
list(d1.keys())
list(d1.values())

# to iterate over both the keys and values, use items to iterate over 2-tuples
list(d1.items())

# you can merge one dictionary into another using .update
d1.update({"b": "foo", "c": 12})
# if you update with same key, the old value will be replaced

# to create dictionaries from sequences
# mapping = {}
# for key, value in zip(key_list, value_list):
#     mapping[key] = value 

# dict() accepts a list of 2-tuples
tuples = zip(range(5), reversed(range(5)))
mapping = dict(tuples)

# sometimes we want to read a dictionary and have a default value
some_dict = {} # some dictionary
# value = some_dict.get(key, default_value)

# suppose we want to group words by their first letter
# we essentially want to make a default value of an empty set for the letters we make

# can do this using setdefault
# by_letter.setdefault(letter, []).append(word) 
# this finds letter in dictionary, if it does not exist, create an empty list, then append word to that list

# can do this using defaultdict
# from collections import defaultdict 
# by_letter = defaultdict(list)
# whenever a missing key is used, automatically create an empty list for it

# valid dictionary key types
# keys generally have to be immutable objects like scalars or tuples
# can check if hashable with hash()
hash("string")

# to use a list as a key, convert it to a tuple
d = {}

d[tuple([1,2,3])] = 5
d 

# ------------------------------------ Set ----------------------------------- #

# an unordered collection of unique elements using set() or {}
set([2, 2, 2, 1, 3, 3])

{2, 2, 2, 1, 3, 3}

# sets support mathematical set operations like union, intersection, difference and symmetric difference
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7, 8}

a.union(b)
a | b # equivalently

a.intersection(b)
a & b

# Set methods
# a.add(x)  : adding x to set
# a.clear() : making set empty
# a.remove(x): removing x
# a.pop() : remove an arbitrary element
# a.union(b) // a | b: union
# a.update(b) // a |= b : set the contents of a to be the union of a and b
# a.intersection(b) : intersection
# a.intersection_update(b) : set the contents of a to be the intersections of the intersection of a and b
# a.difference(b) // a - b : in a but not b
# a.difference_update(b) // a -= b : set a to a diff b
# a.symmetric_difference(b) // a ^ b : all elements in either a or b but not both
# a.symmetric_difference_update(b) // a ^= b : set a to be the symmetric diff
# a.issubset(b) // a <= b : true if a is subset of b
# a.issuperset(b) // a >= b : true if the elements of b are all contained in a
# a.isdisjoint(b) : true if intersection is empty

# ============================================================================ #
#                          Built-in Sequence Functions                         #
# ============================================================================ #

# --------------------------------- enumerate -------------------------------- #
# returns a sequence of (i, value) tuples over an iterable
# for index, value in enumerate(collection):
    # do something with value

# gives both the item and its position just in case you want to do something with position

# ---------------------------------- sorted ---------------------------------- #
# returns a new sorted list from the elements of any sequence
sorted([7,1,2,6,0,3,2])
sorted("horse race")

# ------------------------------------ zip ----------------------------------- #
# pairs up the elements of sequences to create a list of tuples
seq1 = ["foo", "bar", "baz"]
seq2 = ["one", "two", "three"]

zipped = zip(seq1, seq2)
list(zipped)

# if the number of elements don't match, it takes the least number of elements
seq3 = [True, False] 
list(zip(seq1, seq2, seq3))

# a common use of zip is to simultaneously iterate over multiple sequences
for index, (a,b) in enumerate(zip(seq1, seq2)):
    print(f"{index}: {a}, {b}")

# --------------------------------- reversed --------------------------------- #
# iterates over the elements of a sequence in reverse order
list(reversed(range(10)))

# ============================================================================ #
#                   List, Set, and Dictionary Comprehensions                   #
# ============================================================================ #

# ---------------------------- list comprehensions --------------------------- #

# lets you concisely create a new list by filtering the elements of a collection
# [expr for value in collection if condition]
# which is equivalent to 
# result = []
# for value in collection:
#     if condition:
#         result.append(expr)

# the filter condition can be omitted
strings = ["a", "as", "bat", "car", "dove", "python"]

[x.upper() for x in strings if len(x) > 2]
[x for x in strings]

# -------------------- sets and dictionary comprehensions -------------------- #
# dict_comp = {key_expr : value_expr for value in collection if condition}
# set_comp = (expr for value in collection if condition)

unique_lengths = {len(x) for x in strings}

set(map(len, strings))

loc_mapping = {value : index for index, value in enumerate(strings)}

# ------------------------ nested list comprehentions ------------------------ #
all_data = [["John", "Emily", "Michael", "Mary", "Steven"],
            ["Maria", "Juan", "Javier", "Natalia", "Pilar"]]

names_of_interest = []

for names in all_data:
    enough_as = [name for name in names if name.count("a") >= 2]
    names_of_interest.extend(enough_as)

#  you can alternatively wrap all this in a single nested list comperehension
result = [name for names in all_data for name in names if name.count("a") >= 2]

# for names in all_data - iterates over the two lists in all_data
# for name in names if name.count("a") >= 2 - within each list, name matches condition
# leading name puts the string that matches condition into the list

# the for parts are arranged according to the order of nesting 

some_tuples = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
flattened = [x for tup in some_tuples for x in tup]

# the order of the for expressions would be the same if you wrote a nested for loop
flattened = []
for tup in some_tuples:
    for x in tup:
        flattened.append(x)

flattened = [x for tup in some_tuples for x in tup]

# ============================================================================ #
#                                   Functions                                  #
# ============================================================================ #

# def my_function(x, y):
#   return x + y

# if there is no return statement, the function returns None automatically
def function_without_return(x):
    print(x)

result = function_without_return("hello!")

print(result)

# each function can have positional arguments and keyword arguments
def my_function2(x, y, z = 1.5):
    # here z is a keyword argument - specifies default / optional arguments
    if z > 1:
        return z * (x + y)
    else: 
        return z / (x + y)
# x and y are positional (required) arguments
my_function2(5, 6, z = 0.7)
my_function2(3.14, 7, 3.5)

# -------------------- Namespaces, Scope, Local Functions -------------------- #

# functions can access global and local variables
# local variables are those defined within the function
# after the function is finished, the local variable is destroyed

def func():
    a = []
    for i in range(5):
        a.append(i)

# a is created, five elements are appended, and then a is destroyed 

a = [] 
def func():
    for i in range(5):
        a.append(i)

# each call to func will modify list a

# you can assign a global variable within a function, you just need to use the global or nonlocal keywords
a = None 

def bind_a_variable():
    global a 
    a = []
bind_a_variable()

print(a)

# ------------------------- Returning Multiple Values ------------------------ #
def f():
    a = 5
    b = 6
    c = 7
    return a, b, c

a, b, c = f()

# the function is returning a tuple

# alternatively you could return a dictionary instead
def f(): 
    a = 5 
    b = 6
    c = 7
    return {"a" : a, "b" : b, "c" : c}

# --------------------------- Functions are Objects -------------------------- #
states = ["   Alabama ", "Georgia!", "Georgia", "georgia", "FlOrIda",
          "south   carolina##", "West virginia?"]

import re 

def clean_strings(strings):
    result = []
    for value in strings:
        value = value.strip()
        value = re.sub("[!?#]", "", value)
        value = value.title()
        result.append(value)
    return result

# alternatively, you could make  alist of operations to apply to the strings
def remove_punctuation(value):
    return re.sub("[!?#]", "", value)

clean_ops = [str.strip, remove_punctuation, str.title] # list of funcs

def clean_strings(strings, ops):
    result = []
    for value in strings:
        for func in ops:
            value = func(value)
        result.append(value)
    return result 

# you can also use functions as arguments to other functions 

for x in map(remove_punctuation, states):
    print(x)

# map can be used as an alternative to list comprehensions without any filter

# ----------------------- Anonymous (Lambda) Functions ----------------------- #

# writing functions of a single statement 
# defined with the lambda keyword

def short_function(x):
    return x * 2 

# equivalent to
equiv_anon = lambda x: x * 2

# ex1

def apply_to_list(some_list, f):
    return [f(x) for x in some_list]

ints = [4, 0, 1, 5, 6]

apply_to_list(ints, lambda x: x * 2)

# alternatively 
[x * 2 for x in ints]

# ex2 
strings = ["foo", "card", "bar", "aaaa", "abab"]

strings.sort(key = lambda x : len(set(x)))
strings 

# -------------------------------- Generators -------------------------------- #
# iterator is any object that will yield objects for a for loop
# most methods expecting a list or list-like object will also accept any iterator
# e.g. min, max, sum, list, tuple

# a generator constructs a new iterable object using the yield keyword

def squares(n = 10):
    print(f"Generating squares from 1 to {n ** 2}")
    for i in range(1, n+1):
        yield i ** 2
gen = squares()
gen
# no code is immediately executed, only when you request elements from the generator
# does it execute it

for x in gen:
    print(x, end = " ")

# alternatively, you can use a generator expression
gen = (x ** 2 for x in range(100))

gen 

def _make_gen():
    for x in range(100):
        yield x ** 2
gen = _make_gen()

# generator expressions can be used instead of list comprehensions as function arguments
sum(x ** 2 for x in range(100))

dict((i, i **2) for i in range(5))

# note that generators are one-use
gen = (x ** 2 for x in range(3))

list(gen)
# [0, 1, 4]

list(gen)
# []

# ----------------------------- itertools module ----------------------------- #

import itertools 
def first_letter(x):
    return x[0]

# groupby takes a sequence and a function and groups elements in the sequence by 
# the return value of the function

names = ["Alan", "Adam", "Wes", "Will", "Albert", "Steven"]
for letter, names in itertools.groupby(names, first_letter):
    print(letter, list(names))

# some useful itertools functions
# chain(*iterables) - generates a sequence by chaining iterators
# combinations(iterable, k) - generates a sequence of all k-tuples of elements in the iterable ignoring order and without replacement
# permutations(iterable, k) - generates a sequence of all k-tuples in the iterable respecting order
# groupby(iterable[, keyfunc]) - generates (key, sub-iterator) for each unique key
# product(*iterables, repeat=1) - generates the cartesian product of the input iterables as tuples


# ============================================================================ #
#                         Errors and Exception Handling                        #
# ============================================================================ #

# Suppose we want a version of the float() function that fails gracefully
# can use try / except 
def attempt_float(x):
    try: 
        return float(x)
    except:  # only runs if float(x) raises an exception
        return x

attempt_float("1.2345")
attempt_float("something")

# if you want to suppress only a specific kind of error (e.g. ValueError)

def attempt_float(x):
    try: 
        return float(x)
    except ValueError:
        return x 

attempt_float((1,2)) 

# you can catch multiple exceprtion types

def attempt_float(x):
    try: 
        return float(x)
    except (TypeError, ValueError):
        return x 

# alternatively, you may not want some code to be executed regardless of whether try succeeds
# use finally keyword
# that is, run the code no matter whether try succeeded or not
path = ""

def write_to_file(input):
    pass

f = open(path, mode = "w")

try:
    write_to_file(f)
finally:
    f.close()

# you can have code that executes only if the try block succeeds using else
f = open(path, mode = "w")

try: 
    write_to_file(f)
except:
    print("failed")
else:
    print("success")
finally:
    f.close()

# ============================================================================ #
#                         Files in the Operating System                        #
# ============================================================================ #

# ------------------------------ Opening a file ------------------------------ #
# use the open function

path = "examples/segismundo.txt"
f = open(path, encoding = "utf-8")

# by default, the file is opened in read mode, we can treat f as a list and iterate over the lines
for line in f:
    print(line)

lines = [x.rstrip() for x in open(path, encoding = "utf-8")]

# when you use open to create file objects, you should close the file when you are finished with it
# closing the file releases its resources back to the operating system
f.close()

# alternatively, you could use a with statement that automatically closes file
with open(path, encoding = "utf-8"):
    lines = [x.rstrip() for x in f]

# if we type f = open(path, "w"), a new file would be created and overwrite the original file
# the "x" option creates a writable file but fails if the file path already exists

# Python file modes
# r - read only
# w - write only
# x - write only but fails if the file path already exists
# a - appends to existing file
# r+ - read and write
# b - add to mode for binary files
# t - text mode for files

f1 = open(path)
f1.read(10)
f2 = open(path, mode = "rb") # binary mode
f2.read(10)

# the read method advances the file object position by the number of bytes read
# tell gives tyou the current position
f1.tell() # 11
f2.tell() # 10

f1.close()
f2.close()

# file methods
# read([size]) - returns data from file as bytes 
# readable() - returns true if the file can be read
# readline([size]) - returns list of lines in the file
# write(string) - write passed string to file
# writable() - return True if the file can be written
# writelines(strings) - write passed sequence of strings to the file
# close() - close the file
# flush() - flush the internal i/o buffer to disk
# seek(pos) - move to indicated file position 

