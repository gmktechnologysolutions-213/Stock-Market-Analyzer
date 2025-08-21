import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def fetch_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

def calculate_moving_averages(df, windows=[20,50,200]):
    for window in windows:
        df[f'MA_{window}'] = df['Close'].rolling(window=window).mean()
    return df

def calculate_returns_volatility(df):
    df['Daily_Return'] = df['Close'].pct_change()
    volatility = df['Daily_Return'].std() * np.sqrt(252)
    return df, volatility

def plot_stock_analysis(df, ticker):
    plt.figure(figsize=(14,7))
    plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')
    plt.plot(df['Date'], df['MA_20'], label='20-day MA', color='orange')
    plt.plot(df['Date'], df['MA_50'], label='50-day MA', color='green')
    plt.plot(df['Date'], df['MA_200'], label='200-day MA', color='red')
    plt.title(f"{ticker} Stock Price & Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"plots/{ticker}_trend.png")
    plt.show()

    plt.figure(figsize=(10,5))
    sns.histplot(df['Daily_Return'].dropna(), bins=50, kde=True, color='purple')
    plt.title(f"{ticker} Daily Returns Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"plots/{ticker}_returns.png")
    plt.show()

    fig = px.line(df, x='Date', y=['Close','MA_20','MA_50','MA_200'], title=f"{ticker} Stock Price & Moving Averages")
    fig.write_html(f"plots/{ticker}_interactive.html")
    fig.show()

if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g., AAPL): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    df = fetch_stock_data(ticker, start_date, end_date)
    df = calculate_moving_averages(df)
    df, volatility = calculate_returns_volatility(df)

    print(f"Annualized Volatility of {ticker}: {volatility:.2%}")
    print(df.tail())

    plot_stock_analysis(df, ticker)
