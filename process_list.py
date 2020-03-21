import pandas as pd
import numpy as np

df = pd.read_csv("data/TW_share_list.csv")
print(len(df.code.values))