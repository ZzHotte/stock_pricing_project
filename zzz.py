import os
import pandas as pd
from project2 import config as cfg

# ----------------------------------------------------------------------------
# Part 3: Complete the read_prc_csv function
# ----------------------------------------------------------------------------
def read_prc_csv(tic):
    tic = tic.lower()
    pth = os.path.join(cfg.DATADIR,f'{tic}_prc.csv')
    df = pd.read_csv(pth, index_col = 'Date')

    # set the index into datetime data type
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

    return(cfg.standardise_colnames(df))


# ---------------------------------------------------------------------------- 
# Part 4: Complete the mk_prc_df function
# ---------------------------------------------------------------------------- 
def mk_prc_df(tickers, prc_col='adj_close'):
    df_lst = []
    for tic in tickers:
        tic = tic.lower()
        df = read_prc_csv(tic)
        df[tic] = df[prc_col]
        # extract the price colums with corresponding ticker as column index
        prc_col_df = df[[tic]]
        df_lst.append(prc_col_df)

    df_temp = pd.DataFrame()
    df = df_temp.join(df_lst, how = 'outer')
    result = df.dropna(how = 'all').sort_index()

    return(result)

# ---------------------------------------------------------------------------- 
# Part 5: Complete the mk_ret_df function
# ---------------------------------------------------------------------------- 
def mk_ret_df(prc_df):

    # calculate the percentage price change of the input dataframe
    prc_df.sort_index(inplace=True)
    prc_df = prc_df.pct_change()

    # obtain the market price change
    pth = cfg.FF_CSV
    ff_df = pd.read_csv(pth, index_col=0)
    ff_df.index = pd.to_datetime(ff_df.index, format='%Y-%m-%d')

    # extract the mkt price change
    mkt_prc_change = ff_df[['mkt']]

    # join mkt data into original data
    df = prc_df.join(mkt_prc_change, how = 'inner')

    return(df)


# ---------------------------------------------------------------------------- 
# Part 6: Complete the mk_aret_df function
# ---------------------------------------------------------------------------- 
def mk_aret_df(ret_df):

    col_lst = list(ret_df.columns)
    firm_lst = col_lst[:-1]
    empty = ret_df.copy()

    for firm in firm_lst:
        ser1 = ret_df[firm]
        ser2 = ret_df['mkt'].multiply(-1)
        empty[firm] = ser1.add(ser2)

    df = empty.drop('mkt', axis=1)
    return(df)


# ---------------------------------------------------------------------------- 
# Part 7: Auxiliary functions
# ---------------------------------------------------------------------------- 
def get_avg(df, col, year):

    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    data = df.loc[df.index.year == year][col]  # -->series
    ave = data.mean()
    return(ave)


def get_ew_rets(df, tickers):

    df1 = df.dropna(axis = 1, how = 'all')
    df1 = df1[tickers]
    ew = df1.mean(axis = 1) # --> series
    result = ew.dropna()
    return(result)


def get_ann_ret(ser, start, end):

    ser.index = pd.to_datetime(ser.index, format='%Y-%m-%d')
    ser.sort_index(inplace=True)
    ser = ser.dropna()

    daily_ret = ser.loc[start:end]

    num_day = len(daily_ret.index) - 1
    daily_ret.iloc[0] = 0

    # num_day = len(daily_ret.index)

    daily_ret = daily_ret.add(1)
    total_ret = daily_ret.product()
    ann_ret = total_ret ** (252/num_day) - 1

    return(ann_ret)


# ----------------------------------------------------------------------------
# Part 8: Answer the following questions
# ----------------------------------------------------------------------------

# Q1: Which stock in your sample has the highest average daily return for the
#     year 2020 (ignoring missing values)? The sample should include all tickers
#     included in the dictionary config.TICMAP. Your answer should include the
#     ticker for this stock.
Q1_ANSWER = 'TSLA'


# Q2: What is the annualised return for the EW portfolio of all your stocks in
# the config.TICMAP dictionary from the beginning of 2010 to the end of 2020?
Q2_ANSWER = '0.2031357872825712'

# Q3: What is the annualised daily return for the period from 2010 to 2020 for
# the stock with the highest average return in 2020 (the one you identified in
# the first question above)?
Q3_ANSWER = '0.552263158315812'

# Q4: What is the annualised daily ABNORMAL return for the period from 2010 to 2020 for
# the stock with the highest average return in 2020 (the one you identified in
# the first question Q1 above)? Abnormal returns are calculated by subtracting
# the market return ("mkt") from the individual stock return.
Q4_ANSWER = '0.3762854718965194'


# ----------------------------------------------------------------------------
#   Test functions 
# ----------------------------------------------------------------------------

# This is an auxiliary function, please do not modify
def _test_print(obj, msg=None):
    """ Pretty prints `obj`. Will be used by other `_test` functions

    Parameters
    ----------
    obj : any object

    msg : str, optional
        Message preceding obj representation

    """
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
    tickers = ['AAPL', 'TSLA']
    prc_df = mk_prc_df(tickers, prc_col='adj_close')
    _test_print(prc_df)

def _test_mk_ret_df():
    """ Test function for the `mk_ret_df` function

    1. Creates a data frame `prc_df` with prices: 

        | Date       | aapl   | tsla   |
        |------------+--------+--------|
        | 2020-10-13 | 121.09 | 446.64 |
        | 2020-10-14 | 121.19 | 461.29 |
        | 2020-10-15 | 120.70 | 448.88 |
        | 2020-10-16 | 119.01 | 439.67 |
        | 2020-10-12 | 124.40 | NaN    |

    2. Creates the return data frame `ret_df=mk_ret_df(prc_df)`.
       For the `prc_df` data frame above, the `ret_df` data frame should be:

        | Date       | aapl      | tsla      | mkt     |
        |------------+-----------+-----------+---------|
        | 2020-10-12 | NaN       | NaN       | 0.0153  |
        | 2020-10-13 | -0.026608 | NaN       | -0.0041 |
        | 2020-10-14 | 0.000826  | 0.032800  | -0.0065 |
        | 2020-10-15 | -0.004043 | -0.026903 | -0.0008 |
        | 2020-10-16 | -0.014002 | -0.020518 | -0.0006 |

    """
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
    _test_print(ret_df)

    aret_df = mk_aret_df(ret_df)
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
    """ Test function for `get_ew_rets`

    1. Create a test df with the following information:

        |            | tic1 | tic2 | tic3 |
        |------------+------+------+------|
        | 2019-01-01 | 1.0  | 2.0  | 99   |
        | 2019-01-02 | 2.0  | NaN  | 99   |
        | 2020-10-02 | 1.0  | 2.0  | 99   |
        | 2020-11-12 | 2.0  | 1.0  | 99   |
    
    2. Compute the equal-weighted average between tic1 and tic2. For the
    example above, `get_ew_rets(df, ['tic1', 'tic2'])` gives a series with
    the following information:

        | 2019-01-01 | 1.5 |
        | 2019-01-02 | 2.0 |
        | 2020-10-02 | 1.5 |
        | 2020-11-12 | 1.5 |


    """
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
    """ This function will generate a test series with the following
    characteristics:

    - There are 400 obs
    - All values are the same (the daily_yield below)
    - The cumulative return over the 400 days is 50%
    - The datetime index starts in '2010-01-01

    Notes
    -----

    The idea is to work backwards -- figure out what the result should be and
    then construct a test series that will give you this result.

    For instance, assume that you have held a stock for 400 trading days and
    the total return over this period is 1.5 (so 50% over 400 trading days).
    The annualised return you need to compute is:

        tot_ret ** (252/N) - 1 = 1.5 ** (252/400) - 1 = 0.2910

    This should be the result of get_ann_ret if the series contains 400 daily
    returns between some start and end dates with a cumulative return of 50%.

    One possibility is to create a test series with 400 copies of daily_yield,
    where daily_yield is:

        (1 + daily_yield)**400 = 1.5 => daily_yield = 1.5 ** (1/400) - 1 = 0.0010142

    If these were daily returns, the total return would be 1.5

    This means that for a series with 400 copies of daily_yield, with a
    datetime index starting at `start` and ending at `end`, the output of
    `get_ann_ret(ser, start, end)` should be 0.2910.

    This series needs a datetime index starting at some start date and
    spanning 400 days. You can create one using `pd.to_datetime` and
    `pd.to_timedelta`. The `end` date will be the last element in the index.

    """
    tot_ret = 1.5
    n = 400
    start = '2010-01-01'
    daily_yield = tot_ret ** (1.0 / n) - 1

    # This is the expected result (the annualised return)
    exp_res = tot_ret ** (252. / n) - 1

    # Create a series of timedelta objects, representing
    # 0, 1, 2, ... days
    start_dt = pd.to_datetime(start)
    days_to_add = pd.to_timedelta([x for x in range(400)], unit='day')
    idx = start_dt + days_to_add

    # Then create the series
    ser = pd.Series([daily_yield] * n, index=idx)

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

    return ser




def _test_get_ann_ret():
    # Start date
    start = '2010-01-01'
    # Number of trading days
    n = 400
    # series of timedelta (with number of days to add)
    start_dt = pd.to_datetime(start)
    days_to_add = pd.to_timedelta([x for x in range(400)], unit='day')
    idx = start_dt + days_to_add
    ser = _mk_test_ser()
    print(ser)
    end = idx.max().strftime('%Y-%m-%d')
    annual_return = get_ann_ret(ser, start, end)
    _test_print(annual_return, 'Test for the annual return')

if __name__ == "__main__":
    pass
    # _test_cfg()
    # _test_read_prc_csv()
    # _test_mk_prc_df()
    # _test_mk_ret_df()
    # _test_mk_aret_df()
    # _test_get_avg()
    # _test_get_ew_rets()
    # _test_get_ann_ret()


