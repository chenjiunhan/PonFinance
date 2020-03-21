import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import matplotlib.dates as mdates
import requests
import time
import numpy as np
import scipy.signal
from argparse import ArgumentParser
from PonFinance.ponFinance import PonFinance
from collections import defaultdict 
from matplotlib.font_manager import *

def get_change(df, start_date, end_date):

    return (df[df.Date >= end_date].iloc[0].Close - df[df.Date >= start_date].iloc[0].Close) / df[df.Date >= start_date].iloc[0].Close * 100

def get_max_min_date(df, start_date, end_date):

    df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    max_date = df.loc[df.Close.idxmax()].Date
    min_date = df.loc[df.Close.idxmin()].Date
    
    return max_date, min_date

def main(args):
    
    pf = PonFinance(args.market_data_path, args.share_data_path)
    #print(pf.TW_ids)

    changes = {}

    for TW_id in pf.TW_ids:

        try:
            df = pf.read_csv(str(TW_id) + ".TW", "share")
    
            max_date, min_date = get_max_min_date(df, "2020-01-21", "2020-03-14")
            change = get_change(df, max_date, min_date)
            changes[TW_id] = change

        except:
            pass

    TW_share_list = pd.read_csv("/home/jaqq/Workspace/github/PonFinance/data/TW_share_list.csv")
    counter = defaultdict(int)
    sorted_changes = sorted(changes, key=changes.get, reverse=False)

    for k in sorted_changes[:100]:
        print(k, TW_share_list[TW_share_list.code == k].name.values[0], changes[k], TW_share_list[TW_share_list.code == k].group.values[0])
        counter[TW_share_list[TW_share_list.code == k].group.values[0]] += 1
        #counter[] += 1

    for group, num in TW_share_list.group.value_counts().iteritems():
        counter[group] /= num

    #print(counter.items())
    sorted_counter = sorted(counter.items(), key=lambda k_v: k_v[1], reverse=True)
    print(sorted_counter)
    names, values = zip(*sorted_counter)

    #names = list(counter.keys())
    #values = list(counter.values())
    
    myfont = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
    plt.bar(names, values)
    plt.xticks(fontproperties=myfont, rotation=90)
    plt.tight_layout()
    plt.show()


def str2bool(x):
    return x.lower() in ["true"]

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument("--get_data", type=str2bool, default="True")
    parser.add_argument("--market_data_path", type=str, default="/home/jaqq/Workspace/github/PonFinance/data/market")
    parser.add_argument("--share_data_path", type=str, default="/home/jaqq/Workspace/github/PonFinance/data/share")
    args = parser.parse_args()

    main(args)