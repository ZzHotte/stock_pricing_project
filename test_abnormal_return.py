import os
import pandas as pd

from project2 import config as cfg
from project2 import zid_project2 as generate

lst = list(cfg.TICMAP.keys())
ticker_lst = []
for t in lst:
    ticker_lst.append(t.lower())

prc_df = generate.mk_prc_df(ticker_lst, prc_col='adj_close')
ret_df = generate.mk_ret_df(prc_df)

def mk_aret_df(ret_df):
    col_lst = list(ret_df.columns)
    firm_lst = col_lst[:-1]
    empty = pd.DataFrame()
    for firm in firm_lst:
        ser = ret_df[firm] - ret_df['mkt']
        empty[firm] = ser

    df = empty.drop('mkt', axis=1)
    return(ret_df)


df = mk_aret_df(ret_df)

print(ret_df)