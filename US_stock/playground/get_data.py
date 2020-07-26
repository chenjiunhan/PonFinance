import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request as ur
import numpy as np
from pathlib import Path
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import os

def get_income_statement(ticker_symbol, table_type, duration_type):
    
    # table_type: "financials", "balance-sheet", "cash-flow"
    # duration_type: "Annual", "Quarterly"
    
    
    index = ticker_symbol
    url_is = 'https://finance.yahoo.com/quote/' + index + '/' + table_type + '?p=' + index
    print(url_is)

    chrome_options = Options() # 啟動無頭模式
    chrome_options.add_argument('--headless')  #規避google bug
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path="../../web_driver/chromedriver_linux64/chromedriver", options=chrome_options)
    driver.get(url_is)
    driver.implicitly_wait(10)
    
    if duration_type == "Quarterly":
        try:
            print("//span[contains(text(),'" + duration_type + "')]")
            driver.find_element_by_xpath("//span[contains(text(),'" + duration_type + "')]").click()
            time.sleep(5)
        except Exception as e:
            print("B")
            print(e)
            return False

    bool_tgglBtns = True
    while bool_tgglBtns:
        tgglBtns = driver.find_elements_by_xpath('//button[contains(@class, "tgglBtn")]/*[local-name()="svg" and @data-icon="caret-right"]')
        for tgglBtn in tgglBtns:
            #a = tgglBtn.find_element_by_xpath('..')
            #html = driver.execute_script("return arguments[0].innerHTML;", a)
            try:
                tgglBtn.click()
            except Exception as e:
                print(e)
                bool_tgglBtns = False
                continue
        
        time.sleep(1)
        
        if len(tgglBtns) == 0:
            break

    read_data = driver.page_source
    
    soup = BeautifulSoup(read_data,'lxml')
    dates = soup.select("div.D\(tbhg\) span")
    if len(dates) == 0:
        return False
    
    dates_text = []
    for date in dates:
        dates_text.append(date.text)

    fin_rows = soup.select("div.fi-row div")
    if len(fin_rows) == 0:
        return False
    
    data_txt = []
    for tag in fin_rows:
        data_txt.append(tag.text)
    
    data = list(zip(*[iter(data_txt)] * (len(dates_text)+2)))
    
    income_st = pd.DataFrame(data)

    df_income = income_st.T.rename(columns=income_st.T.iloc[0])
    df_income = df_income.drop(df_income.index[[0,1,2]]).reset_index(drop=True)
    df_income.insert(0, "date", dates_text[1:])
    
    return df_income


DATA_PATH = "../data/nasdaq/nasdaq-listed-symbols_csv.csv"
df_symbol = pd.read_csv(DATA_PATH)

display = Display(visible=0, size=(800, 800))  
display.start()

start_from = "CWCO"
start = False
table_types = ["financials", "balance-sheet", "cash-flow"]
duration_types = ["Annual", "Quarterly"]

for symbol in df_symbol.Symbol:    
    for table_type in table_types:
        for duration_type in duration_types:
            if start is False:
                if symbol == start_from:
                    start = True
                else:
                    continue

            print(symbol, table_type, duration_type)
                    
            output_path = "../../data/" + table_type + "/" + duration_type + "/"    
            csv_output_path = output_path + symbol + ".csv"
            
            if os.path.exists(csv_output_path):
                print("exists")
                continue
            
            Path(output_path).mkdir(parents=True, exist_ok=True)
            time.sleep(1 + np.random.rand() * 5)
            
            try:
                df_income = get_income_statement(symbol, table_type, duration_type)
            except Exception as e:
                print(e)
                continue
            
            if df_income is False:
                print("df_income:", df_income)
                continue

            df_income.to_csv(output_path + symbol + ".csv", index=False)
