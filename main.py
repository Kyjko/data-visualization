import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
from matplotlib import style
import matplotlib.pyplot as plt
import datetime

#style.use("ggplot")
with open("key.apikey", "r") as f:
    quandl.ApiConfig.api_key = f.readline().strip("\n")

def visualize_stock_data(reload=True, name="GOOGL"):
    if reload:
        df = quandl.get("WIKI/{}".format(name))
        df.to_csv("{}.csv".format(name))
    else:
        df = pd.read_csv("{}.csv".format(name))

    print(df)
    df["HL_PCT"] = (df["Adj. High"] - df["Adj. Close"]) / df["Adj. Close"] * 100.0
    df["PCT_change"] = (df["Adj. Close"] - df["Adj. Open"]) / df["Adj. Open"] * 100.0

    df = df[["PCT_change", "Adj. Close", "Adj. High", "Adj. Low"]]

    fig, axs = plt.subplots(2)
    axs[0].plot(df[["Adj. Close", "Adj. High", "Adj. Low"]])
    axs[1].plot(df["PCT_change"])

def visualize_forex_data(reload=True, fx="EURHUF"):
    if reload:
        df = quandl.get("CURRFX/{}".format(fx))
        df.to_csv("{}.csv".format(fx))
    else:
        df = pd.read_csv("{}.csv".format(fx))
    
    df.dropna(inplace=True)
    print(df)
    df["MA12"] = df["Rate"].rolling(window=12).mean()
    df["MA26"] = df["Rate"].rolling(window=26).mean()
    df["PCT_change"] = df["Rate"].pct_change()
    df["PCT_change"].dropna(inplace=True)
    df["MA12"].dropna(inplace=True)
    df["MA26"].dropna(inplace=True)
    
    df["Signals"] = [(1 if abs(x-y) <= 0.005 else 0) for x, y in zip(df["MA12"], df["MA26"])]


    fig, axs = plt.subplots(3)
    axs[0].plot(df["Rate"], label="Rate ({})".format(fx))
    axs[0].plot(df["MA12"], label="Moving Average (12)")
    axs[0].plot(df["MA26"], label="Moving Average (26)")
    axs[0].legend(loc="upper left")
    
    axs[1].plot(df["PCT_change"], label="Change")
    axs[1].legend(loc="upper left")
    
      
    axs[2].plot(df["Signals"])

def main():
    visualize_forex_data(reload=False)
    visualize_stock_data(reload=False)
    plt.show()    

if __name__ == "__main__":
    main()


