# Stock_pricing_project

<!--这一部分介绍背景
-------------------------------------------------------------------------------------->
## 01 Background
This assignment project can combine data from multiple CSV files into a single table, calculate individual and abnormal stock returns, and compute returns for a portfolio of stocks.

<!--这一部分介绍构思
-------------------------------------------------------------------------------------->
## 02 Ideas
This project can be broken down into a series of intermediary steps:
* Create a data frame containing the stock price data for multiple companies.
* Calculate returns for each of these companies.
* Subtract the market returns from each individual stock returns to generate abnormal returns.
* Compare the performance of given companies over given period.


<!--这一部分介绍项目里用到的文件 和文件里用到的函数
-------------------------------------------------------------------------------------->
## 03 Functions
### 01 read_prc_csv function
This function creates a data frame with the contents of a CSV file containing stock price information for a given stock ticker.

```
    Parameters
    ----------
        tic : str
            String with the ticker

    Returns
    -------
        df 
        A Pandas data frame containing the stock price information from the CSV
        containing the stock prices for the ticker `tic`.

        This data frame meets the following criteria:
        
        - df.index: `DatetimeIndex` with dates, matching the dates contained in
          the CSV file. The labels in the index must be `datetime` objects.

        - df.columns: each column label will be a column in the CSV file, 
          with the exception of 'Date'. Column names will be formatted
          according to the `standardise_colnames` function included in the
          `project2.config.py` module.
    
    Examples
    --------
    Input stock name and run in the terminal:
        >> tic = 'AAPL'
        >> tic_df = read_prc_csv(tic)
        >> tic_df.info()

        DatetimeIndex: 252 entries, 2010-01-04 to 2010-12-31
        Data columns (total 6 columns):
         #   Column     Non-Null Count  Dtype
        ---  ------     --------------  -----
         0   open       252 non-null    float64
         1   high       252 non-null    float64
         2   low        252 non-null    float64
         3   close      252 non-null    float64
         4   adj_close  252 non-null    float64
         5   volume     252 non-null    int64
        dtypes: float64(5), int64(1)
```  
    


### 02 mk_prc_df function
This function creates a data frame containing price information for a list of tickers and a given type of quote (e.g., open, close, ...).
This function uses the `read_prc_csv` function in this module to read the price information for each ticker in `tickers`.

```
    Parameters
    ----------
    tickers : list
        List of tickers

    prc_col: str, optional
        String with the name of the column we will use to compute returns. The
        column name must conform with the format in the `standardise_colnames`
        function defined in the config.py module.  
        Defaults to 'adj_close'.

    Returns
    -------
    df
        A Pandas data frame containing the `prc_col` price for each stock
        in the `tickers` list:
        
        - df.index: DatetimeIndex with dates. The labels in this index must
          include all dates for which there is at least one valid price quote
          for one ticker in `tickers`.  


        - df.columns: each column label will contain the ticker code (in lower
          case). The number of columns in this data frame must correspond to
          the number of tickers in the ``tickers` parameter. 

    Notes
    -----
    - If the price is not available for a given ticker and date, its value
      will be a NaN, as long as there is a price available for another ticker
      on the same date.

    Examples
    --------
    Example 1: Suppose there are two tickers in `tickers`, "tic1" and "tic2".
    Suppose the following information is available for each ticker: 

      tic1:
          | <date col> | <prc_col> |
          |------------+-----------|
          | 2020-01-02 | 1.0       |

      tic2:
          | <date col> | <prc_col> |
          |------------+-----------|
          | 2020-01-10 | 2.0       |
          | 2020-03-10 | NaN       |

    Then the output data frame will include the following information:

          |            | tic1 | tic2 |
          |------------+------+------|
          | 2020-01-02 | 1.0  | NaN  |
          | 2020-01-10 | NaN  | 2.0  |
    
    The DatetimeIndex will include objects representing the dates 2020-01-02
    and 2020-01-10. The reason 2020-03-10 is not included is because there is
    no price information (for any ticker in `tickers`) on that date.

    Example 2:    

        >> tickers = ['AAPL', 'TSLA']
        >> prc_df = mk_prc_df(tickers, prc_col='adj_close')
        >> prc_df.info()

        <class 'pandas.core.frame.DataFrame'>
        DatetimeIndex: 252 entries, 2010-01-04 to 2010-12-31
        Data columns (total 2 columns):
         #   Column  Non-Null Count  Dtype
        ---  ------  --------------  -----
         0   aapl    252 non-null    float64
         1   tsla    130 non-null    float64
        dtypes: float64(2)

        >> print(prc_df)
                         aapl   tsla
        Date
        2010-01-04   6.604801    NaN
        2010-01-05   6.616219    NaN
        ...               ...    ...
        2010-12-30   9.988830  5.300
        2010-12-31   9.954883  5.326
```


    
### 03 mk_ret_df function
Creates a data frame containing returns for both individuals stock AND 
a proxy for the market portfolio, given a data frame with stock prices, `prc_df`. 

This function will compute returns for each column of `prc_df` and also include the market returns in a column called "mkt".  

Market returns need to be obtained from the "mkt" column in the CSV file "ff_daily_csv". The location of this CSV file is given by the variable `FF_CSV`, defined in the project2.config.py module.
            
```            
    Parameters
    ----------
    prc_df : data frame
        A Pandas data frame with price information (the output of
        `mk_prc_df`). See the docstring of the `mk_prc_df` function
        for a description of this data frame.


    Returns
    -------
    df
        A data frame with stock returns for each ticker in `prc_df` AND the
        returns for the proxy of the overall market portfolio ("mkt").

        - df.index: DatetimeIndex with dates. These dates should include all
          dates in `prc_df` which are also present in the CSV file FF_CSV. 

        - df.columns: Includes all the column labels in `prc_df.columns` AND
          the column label for market returns, "mkt".

    Examples
    --------
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different. 

        >> tickers = ['AAPL', 'TSLA']
        >> prc_df = mk_prc_df(tickers, prc_col='adj_close')
        >> ret_df = mk_ret_df(prc_df)
        >> print(ret_df)

                        aapl      tsla      mkt
        Date
        2010-01-04       NaN       NaN  0.01690
        2010-01-05  0.001729       NaN  0.00310
        ...              ...       ...      ...
        2010-12-30 -0.005011 -0.044356 -0.00111
        2010-12-31 -0.003398  0.004906 -0.00101

        >> ret_df.info()

        <class 'pandas.core.frame.DataFrame'>
        DatetimeIndex: 252 entries, 2010-01-04 to 2010-12-31
        Data columns (total 3 columns):
         #   Column  Non-Null Count  Dtype
        ---  ------  --------------  -----
         0   aapl    251 non-null    float64
         1   tsla    129 non-null    float64
         2   mkt     252 non-null    float64
        dtypes: float64(3)
```     
            
            
    
### 04 mk_aret_df function
Creates a data frame with abnormal returns for each stock in `ret_df`, where abnormal returns are computed by subtracting the market returns from the individual stock returns.

```
    Parameters
    ----------
    ret_df : data frame

        A Pandas data frame with return information for individual stocks and
        the proxy for the overall market portfolio. This data frame is the
        output of `mk_ret_df`.  See the docstring of the `mk_ret_df` function
        for a description of this data frame.

    Returns
    -------
    df
        A data frame with abnormal returns for each individual stock in
        `ret_df`. Abnormal returns are computed by subtracting the market
        returns (column "mkt" in `ret_df`)  from each individual stock's
        returns.

        - df.index: DatetimeIndex with dates. These dates should include all
          dates in the `ret_df` data frame.

        - df.columns: Each column label will be a ticker from the `ret_df`
          (i.e., all the columns of `ret_df` EXCLUDING the column "mkt").

    Examples
    --------
    Note: The examples below are for illustration purposes. Your ticker/sample
    period may be different.

        >> tickers = ['AAPL', 'TSLA']
        >> prc_df = mk_prc_df(tickers, prc_col='adj_close')
        >> ret_df = mk_ret_df(prc_df)
        >> aret_df = mk_aret_df(ret_df)
        >> print(aret_df)

                        aapl      tsla
        Date
        2010-01-04       NaN       NaN
        2010-01-05 -0.001371       NaN
        ...              ...       ...
        2010-12-30 -0.003901 -0.043246
        2010-12-31 -0.002388  0.005916

        >> aret_df.info()

        <class 'pandas.core.frame.DataFrame'>
        DatetimeIndex: 252 entries, 2010-01-04 to 2010-12-31
        Data columns (total 2 columns):
         #   Column  Non-Null Count  Dtype
        ---  ------  --------------  -----
         0   aapl    251 non-null    float64
         1   tsla    129 non-null    float64
        dtypes: float64(2)
        memory usage: 5.9 KB
```            
            
            
            
            
            
### 05 auxiliary functions
Returns the average value of a column for a give year.This function will calculate the average value of the elements included in a column labelled `col` from a data frame `dt`, for a given year `year`. The data frame `df` must have a DatetimeIndex index.

Missing values will not be included in the calculation.

```
    Parameters
    ----------
    df : data frame
        A Pandas data frame with a DatetimeIndex index.

    col : str
        The column label.

    year : int
        The year as a 4-digit integer.

    Returns
    -------
    scalar
        A scalar with the average value of the column `col` for the year
        `year`.

    Example
    -------
    For a data frame `df` containing the following information:

        |            | tic1 | tic2  |
        |------------+------+-------|
        | 1999-10-13 | -1   | NaN   |
        | 1999-10-14 | 1    | 0.032 |
        | 2020-10-15 | 0    | -0.02 |
        | 2020-10-16 | 1    | -0.02 |

        >> res = get_avg(df, 'tic1', 2020)
        >> print(res)
        0.5

        >> res = get_avg(df, 'tic2', 1999)
        >> print(res)
        0.032
```
            
            
            
### 06 get_ew_rets function
Returns a series with the returns on an equally-weighted portfolio of stocks (ignoring missing values).

```
    Parameters
    ----------
    df : data frame
        A Pandas data frame stock returns. Each column label is the stock
        ticker (in lower case).

    tickers : list
        A list of tickers (in lower case) to be included in the portfolio.

    Returns
    -------
    pandas series
        A series with the same DatetimeIndex as the original data frame,
        containing the average of all the columns in `tickers`. The
        equal-weighted average will ignore missing values.

    Example
    -------
    Suppose the input data frame `df` includes the following information:

        |            | tic1 | tic2 | tic3 |
        |------------+------+------+------|
        | 2019-01-01 | 1.0  | 2.0  | 99   |
        | 2019-01-02 | 2.0  | NaN  | 99   |
        | 2020-10-02 | 1.0  | 2.0  | 99   |
        | 2020-11-12 | 2.0  | 1.0  | 99   |

    >> ew = get_we_rets(df, ['tic1', 'tic2'])
    >> print(ew)
    2019-01-01    1.5
    2019-01-02    2.0
    2020-10-02    1.5
    2020-11-12    1.5
    dtype: float64
```


### 07 get_ann_ret function
Returns the annualised returns for a given period.

```
Given a series with daily returns, this function will return the annualised return for the period from `start` to `end` (including `end`).

    Parameters
    ----------
    ser : series
        A Pandas series with a DatetimeIndex index and daily returns.

    start : str
        A string representing the date corresponding to the beginning of the
        sample period in ISO format (YYYY-MM-DD).

    end : str
        A string representing the date corresponding to the end of the
        sample period in ISO format (YYYY-MM-DD).

    Returns
    -------
    scalar
        A scalar with the ANNUALISED return for the period starting in `start`
        and ending in `end`, ignoring missing observations. 

    Notes
    -----
    The annualised return will be computed as follows:

        (tot_ret)**(252/N) - 1

    where 

    - tot_ret represents the total gross return over the period, i.e., the
      product (1+r1)*...*(1+rN), where r1, ..., rN represents daily returns
      from `start` to `end`.

    - N is the number of days WITH NON-MISSING RETURNS (i.e., excluding NaN)
      for the period from `start` to `end`, which were included in the
      computation of tot_ret
        

```   
            

            
<!--如何使用这份文件
-------------------------------------------------------------------------------------->
## 04 User Guide
There project.py can be omported as a module to call the functions in the main script. 
Users can input the name of the stock and the time period they are interested in. The script will produce a dataframe containing cumulative annual returns and abnormal returns.
    
<!--源文件结构
-------------------------------------------------------------------------------------->
## 05 Source Files
All required files are included in the archive with the following structure:
```
    project2/
    | /n
    |__ __init__.py
    |__ config.py
    |__ project_desc.pdf
    |__ zid_project2.py
    |
    |___data/
    | | <many csv files here>
```
where
    
* project2/ represents the main folder containing all the project files.
* zid_project2.py contains the functions you need to write for this project. This is the only file you need to submit.
* project_desc.pdf is the PDF version of this document.
* data/: This is the sub-directory where all the data files for this files are stored. Inside this folder you
will find many files. Each <tic>_prc.csv contains stock price data for the ticker <tic>. These CSV
files include the column names in a header row of text. In addition, this folder contains a file called
ff_daily.csv, which includes market returns.
* config.py is the configuration module for this package. You do not need to modify this file.

