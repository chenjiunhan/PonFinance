import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import requests
import time
import numpy as np
import scipy.signal
from argparse import ArgumentParser
from PonFinance.ponFinance import PonFinance

def main(args):

    pf = PonFinance(args.market_data_path, args.share_data_path)
    pf.get_csvs("share")


    #if args.get_data:
    #    pf.get_csvs()
    #df = pf.read_csv("TWII", "market")
    #print(df)
    #pf.plot_history(df)

def str2bool(x):
    return x.lower() in ["true"]

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument("--get_data", type=str2bool, default="True")
    parser.add_argument("--market_data_path", type=str, default="/home/jaqq/Workspace/github/PonFinance/data/market")
    parser.add_argument("--share_data_path", type=str, default="/home/jaqq/Workspace/github/PonFinance/data/share")
    args = parser.parse_args()

    main(args)