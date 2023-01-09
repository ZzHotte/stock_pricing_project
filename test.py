import os
import pandas as pd

from project2 import config as cfg
from project2 import zid_project2 as generate


if __name__ == "__main__":
    lst = list(cfg.TICMAP.keys())
    ticker_lst = []
    for t in lst:
        ticker_lst.append(t.lower())

    prc_df = generate.mk_prc_df(ticker_lst, prc_col='adj_close')
    ret_df = generate.mk_ret_df(prc_df)
    aret_df = generate.mk_aret_df(ret_df)

    start = '2010-01-01'
    end = '2020-12-31'

    select = 'tsla'

    # #--------------------------------------------------------------

    q1_year = 2020

    # one_year_ret_df = ret_df[ret_df.index.year == q1_year]
    # ave = one_year_ret_df.mean()
    ave = []
    for ticker in ticker_lst:
        ave.append(generate.get_avg(ret_df, ticker, q1_year))

    q1 = ave   # --> maximum value TSLA Q1


    # #-----------------------------------------------------

    # left = 2010
    # right = 2020
    # period = list(range(left, right+1))

    # multiple_year_ret_df = ret_df[ret_df.index.year.isin(period)]
    #
    # ew = generate.get_ew_rets(multiple_year_ret_df, ticker_lst)

    ew = generate.get_ew_rets(ret_df, ticker_lst)

    q2 = generate.get_ann_ret(ew, start, end) # --> portfolio return

    # #------------------------------------------------------

    tsla_ret_ser = ret_df[select]
    q3 = generate.get_ann_ret(tsla_ret_ser,start, end)

    # #------------------------------------------------------

    tsla_aret_ser = aret_df[select]
    q4 = generate.get_ann_ret(tsla_aret_ser, start, end)

    # #----------------------------------------------------------
sep = '\n'
print(f'q2:  {q2}{sep}q3:  {q3}{sep}q4:  {q4}')