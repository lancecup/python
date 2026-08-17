import pandas as pd 
import numpy as np 

# ============================================================================ #
#                      Data and Time Data Types and Tools                      #
# ============================================================================ #
# datetime, time, and calendar modules are places to start

from datetime import datetime 

now = datetime.now()
now 

now.year, now.month, now.day 

# datetime stores both date and time down to the microsecond
# datatime.timedelta represents the temporal difference between two datetime objects
delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
delta 

delta.days
delta.seconds 

# you can add or subtract a timedelta or multiple to a datetime object to get a new datetime
from datetime import timedelta 
start = datetime(2011, 1, 7)
start + timedelta(12)

start - 2 * timedelta(12)

### data types in the datetime module
# date - calendar date
# time - store time of day as hours, minutes, seconds, microseconds
# datetime - both date and time
# timedelta - difference between two datetime values
# tzinfo - base type for storing time zone info

# ------------------ Converting between String and Datetime ------------------ #
stamp = datetime(2011, 1, 3)
str(stamp)

# strftime: datetime -> string
stamp.strftime("%Y-%m-%d")

### datetime format specification
# %Y - four digit year
# %y - two digit year
# %m - two digit month [01, 12]
# %d - two digit day [01, 31]
# %H - Hour -- 24 hour clock [00, 23]
# %I - Hour -- 12 hour [01, 12]
# %M - two digit minute [00, 59]
# %S - Second [00, 61] (60 and 61 are for leap seconds)
# %f - microsecond as an integer
# %j - day of the year [001, 336]
# %w - week day as integer [0 (sunday), 6]
# %u - weekday as integer [1 (monday), 7]
# %U - week number of the year - sunday first day of week
# %W - week number of the year
# %z - UTC time zone offset
# %Z time zone name as string
# %F - shortcut for %Y-%m-%d (2012-04-18)
# %D - shortcut for %m/%d/%y (04/16/12)


# strptime: string -> datetime
value = "2011-01-03"
datetime.strptime(value, "%Y-%m-%d")

datestrs = ["7/6/2011", "8/6/2011"]
[datetime.strptime(x, "%m/%d/%Y") for x in datestrs]

# pandas has a method pd.to_datetime to parse many different kinds of date representations
datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
pd.to_datetime(datestrs)

# it also handles values that should be considered missing
idx = pd.to_datetime(datestrs + [None])
idx  
idx[2] # NaT not a time
pd.isna(idx)

# datetime objects have a number of locale specific formating options
### Locale-specific date formatting
# %a - abbreviated weekday name
# %A - full weekday name
# %b - abbreviated month name
# %B - full month name
# %c - full date and time (Tue 01 May 2012 04:20:57 PM)
# %p - locale equivalent of am or pm
# %x - locale appropriate formatted date (e.g. in the US, May 1, 2012 yields '05/01/2012')
# %X - locale appropriate time ('04:24:12 PM')

# ============================================================================ #
#                              Time Series Basics                              #
# ============================================================================ #
# basic time series object is a series indexed by timestamps 
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5),
         datetime(2011, 1, 7), datetime(2011, 1, 8),
         datetime(2011, 1, 10), datetime(2011, 1, 12)]
ts = pd.Series(np.random.standard_normal(6), index = dates)
ts 

# these datetime objects have been put in a DateTimeIndex
# like other series, arithmetic operations between differently indexed time series align on the dates
ts + ts[::2]
ts.index.dtype # stores data at the nanosecond resolution

# scalar values from DateTimeIndex are Timestamp objects
stamp = ts.index[0]
stamp 

# ---------------------- Indexing, Selection, Subsetting --------------------- #
# time series behaves like any other series when indexing 
stamp = ts.index[2]
ts[stamp]

# you can also pass a string that is interpretable as a date
ts["2011-01-12"]

# for longer time series, a year or only a year and month can be passed to slice data
longer_ts = pd.Series(np.random.standard_normal(1000),
                      index = pd.date_range("2000-01-01", periods = 1000))

longer_ts 

longer_ts["2001"]
longer_ts["2001-05"]

# since most time series is ordered chronologically, you can slice with time stamps not contained in the series to query
ts 
ts["2011-01-06":"2011-01-11"]

# note that indexing gives a view, it is not a separate copy and modifications alter the original

# truncate copies the index and filters based on before or after needed
ts.truncate(after = "2011-01-09")

# this holds true for dfs as well
dates = pd.date_range("2000-01-01", periods=100, freq="W-WED")
long_df = pd.DataFrame(np.random.standard_normal((100, 4)),
                        index=dates,
                        columns=["Colorado", "Texas",
                                "New York", "Ohio"])

long_df.loc["2001-05"]

# -------------------- Time Series with Duplicate Indices -------------------- #
# we can tell that the index is not unique with the is_unique() property
dates = pd.DatetimeIndex(["2000-01-01", "2000-01-02", "2000-01-02",
                          "2000-01-02", "2000-01-03"])
dup_ts = pd.Series(np.arange(5), index = dates)
dup_ts 

dup_ts.index.is_unique

dup_ts["2000-01-03"] # not duplicated
dup_ts["2000-01-02"] # duplicated

# if you wanted to aggregate the data having nonunique timestamps
# can do this by using groupby and pass level = 0
grouped = dup_ts.groupby(level = 0)
grouped.mean()

# ============================================================================ #
#                    Date Ranges, Frequencies, and Shifting                    #
# ============================================================================ #

# generic time series are assumed to be irregular (no fixed frequency)
# sometimes might want to work relative to a fixed frequency even if have NAs
ts 
resampler = ts.resample("D") # force into fixed daily frequency with resample()
resampler 

# -------------------------- Generating Date Ranges -------------------------- #
# pd.date_range() generates a DatetimeIndex with an indicated length according to a frequency
index = pd.date_range("2012-04-01", "2012-06-01")
index 

# daily by default

#you can pass number of periods to generate if not start and end date
pd.date_range(start = "2003-01-10", periods = 24)
pd.date_range(end = "2020-03-25", periods = 100)

# if you want a date index containing the last business day of each month,
# can pass "BM" frequency - business end of month

# Current pandas frequency aliases

# D       # calendar day
# B       # business day

# h       # hour                 OLD: H
# min     # minute               OLD: T
# s       # second               OLD: S

# ME      # month end            OLD: M
# BME     # business month end   OLD: BM
# MS      # month start          unchanged
# BMS     # business month start unchanged

# W-MON   # weekly on Monday
# W-TUE   # weekly on Tuesday
# W-WED   # weekly on Wednesday
# # etc.

# WOM-1MON   # first Monday of month
# WOM-2MON   # second Monday of month
# WOM-3FRI   # third Friday of month

# QE-JAN     # quarter end, fiscal year ending January    OLD: Q-JAN
# BQE-JAN    # business quarter end                       OLD: BQ-JAN
# QS-JAN     # quarter start                              unchanged
# BQS-JAN    # business quarter start                     unchanged

# YE-JAN     # year end                                   OLD: A-JAN / Y-JAN
# BYE-JAN    # business year end                          OLD: BA-JAN / BY-JAN
# YS-JAN     # year start                                 OLD: AS-JAN
# BYS-JAN    # business year start                        OLD: BAS-JAN

# date_range preserves the time of the start or end timestamp
pd.date_range("2012-05-02 12:56:31", periods = 5)

# sometimes you'll have dates with time but just want to normalize it to midnight
# use normalize option
pd.date_range("2012-05-02 12:56:31", periods = 5, normalize = True)

# ----------------------- Frequencies and Date Offsets ----------------------- #
# for each base frequency, there is a date offset
# e.g. hourly frequency, we can define a multiple of an offset by passing an integer
from pandas.tseries.offsets import Hour, Minute 
hour = Hour() 
hour 
four_hours = Hour(4)
four_hours 

# but realistically you can just use a string alia like "H" or "4H"
# putting an integer before the base frequency creates a multiple
pd.date_range("2000-01-01", "2000-12-31 23:59", freq = "4h")

pd.date_range("2000-1-01", "2000-12-31 23:59", freq = "1h30min")

# Week of month dates
monthly_dates = pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI")
list(monthly_dates)

# -------------------- Shifting (Leading and Lagging Data) ------------------- #
# shift method shifts forward or backward leaving the index unmodified

ts = pd.Series(np.random.standard_normal(4),
                index=pd.date_range("2000-01-01", periods=4, freq="ME"))
ts 
ts.shift(2)
ts.shift(-2)

# can calculate consecutive percent changes in a time series or multiple time series as df cols
ts / ts.shift(1) - 1 

# if the frequency is known, pass it to shift to advance the time stamps instead og just the data
ts.shift(2, freq = "ME")
ts.shift(3, freq = "D")
ts.shift(1, freq = "90min")

# shifting dates with offsets
# pd date offsets can also be used with dattime or Timestamp objects
from pandas.tseries.offsets import Day, MonthEnd 
now = datetime(2011, 11, 17)
now + 3 * Day()

# if you add an anchored offset like MonthEnd, the first increment will roll forward a date according to the rule
now + MonthEnd()
now + MonthEnd(2)

# anchored offsets can explicitly roll dates forward or backward by using their rollforward and rollback methods
offset = MonthEnd()
offset.rollforward(now)
offset.rollback(now)

## Can use offsets with groupby
ts = pd.Series(np.random.standard_normal(20),
                index=pd.date_range("2000-01-15", periods=20, freq="4D")
)

ts.groupby(MonthEnd().rollforward).mean()

# alternatively could just resample
ts.resample("ME").mean()

# ============================================================================ #
#                              Time Zone Handling                              #
# ============================================================================ #

import pytz 

tz = pytz.timezone("America/New_York")
tz 

# ------------------- Time Zone Localization and Conversion ------------------ #
# time series are time zone naive by default
dates = pd.date_range("2012-03-03 09:30", periods = 6)
ts = pd.Series(np.random.standard_normal(len(dates)), index = dates)
ts 
print(ts.index.tz)

pd.date_range("2012-03-09 09:30", periods = 10, tz = "UTC") # manually setting tz

# converting from naive to localized is by tz_localize()
ts 
ts_utc = ts.tz_localize("UTC")
ts_utc.index 

# once localized, can be converted to another
ts_utc.tz_convert("America/New_York")

# we could localize to US East then to UTC
ts_eastern = ts.tz_localize("America/New_York")
ts_eastern.tz_convert("UTC")
ts_eastern.tz_convert("Europe/Berlin")

# ============================================================================ #
#                      Resampling and Frequency Conversion                     #
# ============================================================================ #
# converting a time series from one frequency to another
# high frequency -> low frequency - downsampling
# vice versa - upsampling

# pd objects have a resample method 
# you call resample to group the data, then call an aggregation function 
dates = pd.date_range("2000-01-01", periods = 100)
ts = pd.Series(np.random.standard_normal(len(dates)), index = dates)

ts.resample("ME").mean()
ts.resample("ME").mean().to_period("M") # converting index to monthly

### resample method arguments
# rule - target resampling frequency
# closed - which side of each interval is inclusive ("left" or "right")
# label - which edge is used to label resulting interval ("left" or "right")
# convention - whether to use "start" or "end" of the peripd
# on - df col to resample
# level - for a multiindex, the datetime-like level to resample
# origin - reference timestamp to determine bin boundaries
# offset - time offset added to origin
# group_keys - whether group_keys are included when using .apply()