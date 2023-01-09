""" zid_project2.py

"""
# ---------------------------------------------------------------------------- 
# Part 1: Read the documentation for the following methods:
#   - pandas.DataFrame.mean
#   - pandas.Series.add
#   - pandas.Series.prod
#   - pandas.Series.dropna
# ---------------------------------------------------------------------------- 

import os

import string

import math

import pandas as pd

from project2 import config as cfg

# ---------------------------------------------------------------------------- 
# Part 2: import the config module inside the project2 package
# ---------------------------------------------------------------------------- 
# Create an import statement so that the module config.py (inside the project2 
# package) is imported as "cfg"
# Note: This module should be imported as cfg
#
# <COMPLETE THIS PART>


# ---------------------------------------------------------------------------- 
# Part 3: Complete the read_prc_csv function
# ---------------------------------------------------------------------------- 
def read_prc_csv(tic):
    
    # <COMPLETE THIS PART>

    # create the path string for csv files
    tic = tic.lower()
    name = tic+ "_prc.csv"
    pth = cfg.DATADIR + "/" + name

    # read csv files
    fmt = '%Y-%m-%d'
    # df = pd.read_csv(pth,  parse_dates = ["Date"], index_col=["Date"])

    df = pd.read_csv(pth)
    df.loc[:,"Date"] = pd.to_datetime(df.loc[:,"Date"], format = fmt)
    df.set_index("Date", inplace = True)

    return df


# ---------------------------------------------------------------------------- 
# Part 4: Complete the mk_prc_df function
# ---------------------------------------------------------------------------- 
def mk_prc_df(tickers, prc_col='adj_close'):
    
    # <COMPLETE THIS PART>
    # get the first dataframe
    prc_col = prc_col.replace("_", " ")
    prc_col = string.capwords(prc_col)

    # handle the first ticker
    summary = read_prc_csv(tickers[0])[[prc_col]]

    #change column name
    name = tickers[0].lower()
    summary.columns = [name]

    # use for loop to merge the rest of tickers
    for i in range (len(tickers)):
        if i == 0:
            i + 1
        else:
            temp_data = read_prc_csv(tickers[i])[[prc_col]]
            col_name = tickers[i].lower()
            temp_data.columns = [col_name]
            # full outer join the stock so no data lost
            summary = summary.merge(temp_data, how = 'outer', left_index = True, right_index = True)

    return summary


# ---------------------------------------------------------------------------- 
# Part 5: Complete the mk_ret_df function
# ---------------------------------------------------------------------------- 
def mk_ret_df(prc_df):
    
    # <COMPLETE THIS PART>

    #  create dataframe for market data
    market_data = pd.read_csv(cfg.FF_CSV)
    market_data.loc[:,"Date"] = pd.to_datetime(market_data.loc[:,"Date"], format ='%Y-%m-%d')
    market_data.set_index("Date", inplace = True)

    #convert price to return
    market_data = market_data[['mkt']]

    # Sort the input data to avoid calculation mistakes
    prc_df.sort_index(inplace=True)

    # Calculate the return for stocks
    prc_df = prc_df.pct_change(1)

    # merge the market dataframe with the stocks' dataframe
    prc_df = prc_df.merge(market_data, how = 'left', left_index = True, right_index = True)
    prc_df.sort_index(inplace = True)

    return prc_df



# ---------------------------------------------------------------------------- 
# Part 6: Complete the mk_aret_df function
# ----------------------------------------------------------------------------
def mk_aret_df(ret_df):
    
    # <COMPLETE THIS PART>
    # abnormal return = stock return - market return
    tickers = list(ret_df.columns)

    for i in range (len(tickers)):
        if tickers[i] != 'mkt':
            ret_df[tickers[i]] = ret_df[tickers[i]] - ret_df['mkt']


    ret_df.drop('mkt', inplace=True, axis=1)



    return ret_df

# ---------------------------------------------------------------------------- 
# Part 7: Auxiliary functions
# ---------------------------------------------------------------------------- 
def get_avg(df, col, year):
    
    #<COMPLETE THIS PART>

    single = df[[col]]

    # single = single + 1
    # years_ave = single.groupby([single.index.year]).mean()

    # convert date formate
    start = str(year) + "-01-01"
    end = str(year) + "-12-31"
    fmt = '%Y-%m-%d'
    start = pd.to_datetime(start, format = fmt)
    end = pd.to_datetime(end, format = fmt)

    # crop the dataframe to desired time frame
    year_data = single.loc[start:end]

    # get the available date list
    dateList = list(year_data.index)
    # calculate the number of days in the stock series
    number_of_days = len(dateList)
    # minus the days that have NaN values to get the true duration
    duration = number_of_days - year_data.isnull().values.ravel().sum()

    # convert series to 1 + return
    year_data = year_data + 1

    # Use a for loop to calculate the total return
    tot_ret = 1
    for i in range (len(year_data)):
        if (math.isnan (year_data.iloc[i].values[0])is False):
            tot_ret = tot_ret * year_data.iloc[i].values[0]

    # Calculate the annualised return
    annualized_ret = tot_ret ** (252/duration) - 1



    # print(years_ave)

    #
    # temp = years_ave.loc[[year]]
    # mean = temp.iat[0,0]
    # return mean
    return annualized_ret


def get_ew_rets(df, tickers):
    
    #<COMPLETE THIS PART>

    df = df[tickers].mean(axis=1)
    return df

def get_ann_ret(ser, start, end):
    
    # <COMPLETE THIS PART>

    # crop the series to desired time frame
    ew = ser.loc[start:end]

    # get the available date list
    dateList = list(ew.index)
    # calculate the number of days in the stock series
    number_of_days = len(dateList)
    # minus the days that have NaN values to get the true duration
    duration = number_of_days - ew.isnull().values.ravel().sum()

    # convert series to 1 + return
    ew = ew + 1

    # Use a for loop to calculate the total return
    tot_ret = 1

    for i in range (len(ew)):
        if (math.isnan (ew.iloc[i])is False):
            tot_ret = tot_ret * ew.iloc[i]


    # Calculate the annualised return
    annualized_ret = tot_ret ** (252/duration) - 1

    return annualized_ret



# ----------------------------------------------------------------------------
# Part 8: Answer the following questions
# ----------------------------------------------------------------------------
# NOTES:
# 
# - You can create a separate module (you can call it main.py if you want) 
#   and then use the functions defined above to answer the questions below. 
#   YOU DO NOT NEED TO SUBMIT THIS OTHER MODULE YOU CREATE. THE ONLY MODULE
#   YOU NEED TO SUBMIT IS THIS ONE, zid_project2.py.
#
# - Do not create any other functions inside this module. 
# 
# - For this part of the project, only the answers provided below will be
#   marked. You are free to create any function you want (IN A SEPARATE
#   MODULE).
#
# - All your answers should be strings. If they represent a number, include 4
#   decimal places.
# 
# - Here is an example of how to answer the questions below. Consider the
#   following question:
#
#   Q0: Which ticker included in config.TICMAP starts with the letter "C"?
#   Q0_answer = '?'
#  
#   You should replace the '?' with the correct answer:
#   Q0_answer = 'CSCO'
#  

# Q1: Which stock in your sample has the highest average daily return for the
#     year 2020 (ignoring missing values)? The sample should include all tickers
#     included in the dictionary config.TICMAP. Your answer should include the
#     ticker for this stock.
Q1_ANSWER = 'TSLA'


# Q2: What is the annualised return for the EW portfolio of all your stocks in
# the config.TICMAP dictionary from the beginning of 2010 to the end of 2020?
Q2_ANSWER = 0.20435428936872047

# Q3: What is the annualised daily return for the period from 2010 to 2020 for
# the stock with the highest average return in 2020 (the one you identified in
# the first question above)?
Q3_ANSWER = 0.5516209538619083

# Q4: What is the annualised daily ABNORMAL return for the period from 2010 to 2020 for
# the stock with the highest average return in 2020 (the one you identified in
# the first question Q1 above)? Abnormal returns are calculated by subtracting
# the market return ("mkt") from the individual stock return.
Q4_ANSWER = 0.3770885290285164


# ----------------------------------------------------------------------------
#   Test functions 
# ----------------------------------------------------------------------------

# This is an auxiliary function, please do not modify
def _test_print(obj, msg=None):
    
    import pprint as pp
    sep = '-'*40
    if isinstance(obj, str):
        prt = obj
    else:
        prt = pp.pformat(obj)
        prt = f'{prt}\n\nObj type is: {type(obj)}'
    if msg is not None:
        prt = f'{msg}\n\n{prt}'
    to_print = [
        '',
        sep,
        prt,
        ]
    print('\n'.join(to_print))
    if isinstance(obj, pd.DataFrame):
        print('')
        obj.info()
    print(sep)

# This is an auxiliary function, please do not modify


def _test_cfg():
    """ Tests if the config.py module inside the project2 package
    was successfully imported as `cfg`

    toolkit/
    |
    |__ project2/
    |   |__ data/       <-- project2.config.DATADIR
    |
    """
    # Test if the data folder is inside the project2 folder
    # NOTE: The "parent" of the `data` folder is `project2`
    parent = os.path.dirname(cfg.DATADIR)
    to_print = [
        'The variable `parent` should point to the project2 folder: ',
        f'  parent: {parent}',
        f'  Folder exists: {os.path.exists(parent)}',
        '',
        'The data folder for this project is located at:',
        f'  cfg.DATADIR: {cfg.DATADIR}',
        f'  Folder exists: {os.path.exists(cfg.DATADIR)}',
        ]
    _test_print('\n'.join(to_print))


def _test_read_prc_csv():
    """ Test function for `read_prc_csv`
    """
    tic = 'TSLA'
    df = read_prc_csv(tic)
    _test_print(df)


def _test_mk_prc_df():
    """ Test function for `mk_prc_df`
    """
    tickers = ['AAPL', 'TSLA','PG']
    prc_df = mk_prc_df(tickers, prc_col='adj_close')
    _test_print(prc_df)

def _test_mk_ret_df():
    
    # Test data frame
    prc_df = pd.DataFrame({
        'aapl': [
            121.09, 
            121.19, 
            120.70, 
            119.01,
            124.40, 
            ],
        'tsla': [
            446.64, 
            461.29, 
            448.88, 
            439.67,
            None, 
            ],
        },
        index=pd.to_datetime([
            '2020-10-13', 
            '2020-10-14', 
            '2020-10-15', 
            '2020-10-16',
            '2020-10-12', 
            ],
        ))
    msg = "The input data frame `prc_df` is:"
    _test_print(prc_df, msg=msg)

    msg = "The output data frame `ret_df` is:"
    ret_df = mk_ret_df(prc_df)
    _test_print(ret_df, msg=msg)

    # tickers = ['AAPL', 'TSLA', 'PG']
    # data = mk_prc_df(tickers, prc_col='adj_close')
    # temp = mk_ret_df(data)
    # _test_print(temp, msg=msg)


def _test_mk_aret_df():
    """ Test function for the `mk_aret_df` function

    1. Creates a data frame `ret_df` with returns: 

        |            | aapl      | tsla      | mkt     |
        |------------+-----------+-----------+---------|
        | 2020-10-12 | NaN       | NaN       | 0.0153  |
        | 2020-10-13 | -0.026608 | NaN       | -0.0041 |
        | 2020-10-14 | 0.000826  | 0.032800  | -0.0065 |
        | 2020-10-15 | -0.004043 | -0.026903 | -0.0008 |
        | 2020-10-16 | -0.014002 | -0.020518 | -0.0006 |

    2. Creates the abnormal return data frame `aret_df=mk_aret_df(ret_df)`.
       For the `ret_df` data frame above, the `aret_df` data frame should be:

        |            | aapl      | tsla      |
        |------------+-----------+-----------|
        | 2020-10-12 | NaN       | NaN       |
        | 2020-10-13 | -0.022508 | NaN       |
        | 2020-10-14 | 0.007326  | 0.039300  |
        | 2020-10-15 | -0.003243 | -0.026103 |
        | 2020-10-16 | -0.013402 | -0.019918 |

    """
    idx = pd.to_datetime([
        '2020-10-12', 
        '2020-10-13', 
        '2020-10-14', 
        '2020-10-15', 
        '2020-10-16', 
        ])
    aapl = [
        None, 
        -0.026608, 
         0.000826, 
        -0.004043, 
        -0.014002, 
        ]
    tsla = [
        None, 
        None,
         0.032800,
        -0.026903,
        -0.020518,
        ]
    mkt = [
      0.0153,
     -0.0041,
     -0.0065,
     -0.0008,
     -0.0006,
     ]
    ret_df = pd.DataFrame({'aapl': aapl, 'tsla': tsla, 'mkt': mkt,}, index=idx)
    print("\nThe input data frame 'ret_df' is:")
    _test_print(ret_df)


    aret_df = mk_aret_df(ret_df)
    print("\nThe output data frame 'ret_df' is:")
    _test_print(aret_df)


def _test_get_avg():
    """ Test function for `get_avg`
    """
    # Made-up data
    prc = pd.Series({
        '2019-01-01': 1.0,
        '2019-01-02': 2.0,
        '2020-10-02': 4.0,
        '2020-11-12': 4.0,
        })
    df = pd.DataFrame({'some_tic': prc})
    df.index = pd.to_datetime(df.index)
    
    msg = 'This is the test data frame `df`:'
    _test_print(df, msg)


    res = get_avg(df, 'some_tic', 2019)
    to_print = [
            "This means `res =get_avg(df, col='some_tic', year=2019) --> 1.5",
            f"The value of `res` is {res}",
            ]
    _test_print('\n'.join(to_print))
    

def _test_get_ew_rets():
    
    # Made-up data
    tic1 = [1.0, 2.0, 1.0, 2.0,]
    tic2 = [2.0, None, 2.0, 1.0,]
    tic3 = [99, 99, 99, 99,]
    idx = pd.to_datetime(['2019-01-01', '2019-01-02', '2020-10-02', '2020-11-12'])
    df = pd.DataFrame({'tic1': tic1, 'tic2': tic2, 'tic3': tic3}, index=idx)
    msg = 'This is the test data frame `df`:'
    _test_print(df, msg)

    ew_ret = get_ew_rets(df, ['tic1', 'tic2'])
    msg = "The output of get_ew_rets(df, ['tic1', 'tic2']) is:"
    _test_print(ew_ret, msg)


def _mk_test_ser():
    
    tot_ret = 1.5
    n = 400
    start = '2010-01-01'
    daily_yield = tot_ret**(1.0/n)-1

    # This is the expected result (the annualised return)
    exp_res = tot_ret ** (252./n) - 1

    # Create a series of timedelta objects, representing
    # 0, 1, 2, ... days
    start_dt = pd.to_datetime(start)
    days_to_add = pd.to_timedelta([x for x in range(400)], unit='day')
    idx = start_dt + days_to_add

    # Then create the series
    ser = pd.Series([daily_yield]*n, index=idx)

    # So, `get_ann_ret(ser, start, end) --> exp_res`
    # We have the `ser` and `start`. What about `end`?
    end = ser.index.max().strftime('%Y-%m-%d')

    to_print = [
        f"Given the parameters:",
        f"   - tot_ret is {tot_ret}",
        f"   - N is {n}",
        f"   - start is '{start}'",
        f"   - end is '{end}'",
        f" For the period from '{start}' to '{end}'",
        f" the annualised return is: {exp_res}",
        "",
        f"For the `ser` below, `get_ann_ret(ser, '{start}', '{end}')` --> {exp_res}",
    ]
    print('\n'.join(to_print))
    print(ser)

    return ser


if __name__ == "__main__":
    pass
    # _test_cfg()
    # _test_read_prc_csv()
    # _test_mk_prc_df()
    # _test_mk_ret_df()
    # _test_mk_aret_df()
    # _test_get_avg()
    _test_get_ew_rets()
    # _test_get_ann()




    ser = _mk_test_ser()

    #### Part 8: Question 1 ####
    tickers = cfg.TICKERS
    df = mk_prc_df(tickers, prc_col='adj_close').pct_change(1)
    value_set = []
    name = []
    for i in range(len(tickers)):
        tickers[i] = tickers[i].lower()
        name.append(tickers[i])
        value_set.append(get_avg(df, tickers[i], 2020))

    # Create a dictionary to stare data
    zip_dic = zip(name,value_set)
    compare_dic = dict(zip_dic)

    # Find out the stock with the highest return
    max_key = max(compare_dic, key=compare_dic.get)
    print("Best performed stock: " + max_key)
    print("It's averaged return on 2020: " + str(compare_dic[max_key]))
    print("\n")

    #### Part 8 Question 2 ####

    # Get the equal weighted portfolio return
    ew_port = get_ew_rets(df, tickers)

    port_ret = get_ann_ret(ew_port,"2010-01-01", "2012-12-31")
    print("Annualised portfolio return the beginning of 2010 to the end of 2020:")
    print(port_ret)

    #### Part 8 Question 3 ####
    tsla_series = mk_prc_df(['v','TSLA'], prc_col='adj_close').pct_change(1)
    tsla_series = tsla_series['v']


    ann_ret = get_ann_ret(tsla_series, '2010', '2012')

    print("tsla annualised return:")
    print(ann_ret)

    #### Part 8 Question 4 ####
    tsla_again = mk_prc_df(['v','TSLA'], prc_col='adj_close')
    tsla_again = mk_ret_df(tsla_again)


    tsla_again = mk_aret_df(tsla_again)
    tsla_series = tsla_again['v']


    abnormal_ret = get_ann_ret(tsla_series, '2010', '2012')
    print("annualised abnormal return for tsla fomr 2010 to 2020:")
    print(abnormal_ret)

