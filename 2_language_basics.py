# Python uses indentation to structure code 
# A semicolon lets you make multiple statements in one line, but it is not recommended to use it in Python code.

# Everything is a python object 

# Almost every object has attached functions (methods)
# object.some_method(x,y,z)

# When assigning an object a to another object b, they both point to the same object, b is not a separate copy
a = [1, 2, 3]
b = a 
b
a.append(4)
b

# when you use an object as an argument for a function, it refers to teh same object
def append_element(some_list, element):
    some_list.append(element)

data = [1, 2, 3]
append_element(data, 4)
data

# you can check the type of an object using isinstance()
a = 5; b = 4.5 

isinstance(a, int) # True
isinstance(a, (int, float)) # checks for either int or float 
isinstance(b, (int, float)) # True

# Attributes and methods
# - Attributes - other python objects stores inside the object
# - Methods - functions associated with an object that can have access to the object's internal data 

a = "foo"
# a.<Press_Tab> will show the attributes and methods associated with the string object a


# Duck typing means python cares about what an object can do
# that is, making functions that can work with any object that has the right methods and attributes, rather than checking for a specific type of object.

# you can import from other scripts to use objects defined in that other script

# Binary operators 
# a + b  : add
# a - b  : subtract
# a * b  : multiply
# a / b  : divide
# a // b : dropping fractional part in division
# a ** b : a^b
# a & b  : AND 
# a | b  : OR 
# a ^ b  : if a or b is true but not both
# a == b : equal 
# a != b : not equal 
# a < b  : less than
# a <= b : less than or equal to
# a > b  : greater than
# a >= b : greater than or equal to
# a is b : if a and b reference the same object
# a is not b : if different python objects 

# Mutable and Immutable objects
# Mutable objects can be changed: lists, sets, dictionaries
# Immutable objects cannot be changed: strings, tuples, numbers

# Scalar Types 
# None, str, bytes, float, bool, int

# some string functions
a = "this is a string"
b = a.replace("string", "new string") # replaces the first argument with the second argument
b # only b is defined, a is unchanged since strings are immutable

a = 5.6
s = str(a) # convert to string
s

# leading a string with r makes it interpreted as-is
# since backslashes are used for escape characters, 
s = "12\34"
s 

s = r"this\has\no\special\characters"
s

# adding two strings concatenates them

# string templating / formating
template = "{0:.2f} {1:s} are worth US${2:d}"
# {0:.2f} means to format the first argument as a floating point with two decimal points
# {1:s} is to format the second argument as a string
# {2:d} means to format the third argument as an integer

# for f strings, same principle applies

amount = 10
rate = 88.46
currency = "pesos"
result = f"{amount} {currency} are worth US${amount/rate:.2f}"

# Type casting 
# str(), bool(), int(), float() 

# Dates and times
#  the built in datetime module provides datetime, date, and time types
from datetime import datetime, date, time
dt = datetime(2011, 10, 29, 20, 30, 21)
dt.day
dt.minute
dt.date()
dt.time()

dt.strftime("%Y-%m-%d %H:%M") # converts datetime as a string

# strings can be converted to datetime objects with strptime()
datetime.strptime("20091031", "%Y%m%d")

#  you can set time with .replace when aggregating
dt_hour = dt.replace(minute=0, second=0)

# the difference of datetime objects produces a timedelta type
dt2 = datetime(2011, 11, 15, 22, 30)
delta = dt2 - dt
delta 
type(delta)

# adding a timedelta to a datetime produces a new shifted datetime

# ============================================================================ #
#                                 Control Flow                                 #
# ============================================================================ #

# if, elif, else

x = -5 
if x < 0: 
    print("negative")

if x < 0:
    print("negative")
elif x == 0:
    print("zero")
elif 0 < x < 5:
    print("positive < 5")
else: 
    print("positive >= 5")

# for loops

sequence = [1, 2, None, 4, None, 6]
total = 0
for value in sequence:
    if value is None:
        continue
    total += value
total

# can be broken with break but it only breaks the inner most for loop not the whole thing if nested

# while loops
# runs until condition is false

x = 256 
total = 0 
while x > 0:
    if total > 500:
        break
    total += x 
    x = x // 2
x

# pass does nothing, used for blocks where no action is to be taken

# range generates a sequence of integers
# range(start, end-1, step)

# we can iterate through sequences by index
seq = [1, 2, 3, 4, 5]
for i in range(len(seq)):
    print(f"element {i} of the sequence is {seq[i]}")

