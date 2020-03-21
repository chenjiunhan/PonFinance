import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import requests
import time
import numpy as np
import scipy.signal
import os

class PonFinance():
    
    def __init__(self, market_data_path = "/home/jaqq/Workspace/github/PonFinance/data/market", 
                       share_data_path = "/home/jaqq/Workspace/github/PonFinance/data/share"):
        self.market_data_path = market_data_path
        self.share_data_path = share_data_path
        self.markets = [
                        "TWII",
                        "DJI",
                        "IXIC"
                       ]
        self.TW_ids = np.load("/home/jaqq/Workspace/github/PonFinance/data/share/TW_ids/TW_ids.npy")
    
    def save_csv(self, url, output_path):
        
        r = requests.get(url, allow_redirects=True)
        open(output_path, 'wb').write(r.content)

        return output_path
    
    def get_csv(self, name, category):
      
        if category == "market":
            prefix = "%5E"
            output_path = self.market_data_path + os.sep + name + ".csv"
        elif category == "share":
            prefix = ""
            output_path = self.share_data_path + os.sep + "TW" + os.sep + name + ".csv"

        start_ts = str(0)    
        end_ts = str(int(time.time()))
        url = "https://query1.finance.yahoo.com/v7/finance/download/" + prefix + name + "?period1=" + start_ts + "&period2=" + end_ts + "&interval=1d&events=history"

        self.save_csv(url, output_path)
        print("Get", name, "to", output_path)

    def get_csvs(self, category):

        if category == "market":
            for market in self.markets:
                time.sleep(10 + np.random.rand()*3)
                self.get_csv(market, category)
        elif category == "share":
            for TW_id in self.TW_ids:
                if TW_id < 3665:
                    continue
                time.sleep(1 + np.random.rand()*3)
                self.get_csv(str(TW_id) + ".TW", category)
        else:
            print("No such category")

    def read_csv(self, name, category):

        if category == "market":
            csv_path = self.market_data_path + os.sep + name + ".csv"
        elif category == "share":
            csv_path = self.share_data_path + os.sep + "TW" + os.sep + name + ".csv"

        return pd.read_csv(csv_path)
    
    def plot_history(self, df):
        x_values = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in df.Date.values]
        formatter = mdates.DateFormatter("%Y-%m-%d")

        if df.shape[0] > 365 * 6:
            locator = mdates.YearLocator()
        elif df.shape[0] > 60:
            locator = mdates.MonthLocator()
        else:
            locator = mdates.DayLocator()

        plt.figure(figsize=(20,3))
        ax = plt.gca()
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(locator)
        plt.plot(x_values, df.Close)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.grid()
        plt.show()