import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データのダウンロード
sp500_data = yf.download('^GSPC', start='1994-01-01', end='2023-12-31', interval='1mo')
bond_data = yf.download('^TNX', start='1994-01-01', end='2023-12-31', interval='1mo')

# 月次リターンの計算
sp500_data['Return'] = sp500_data['Adj Close'].pct_change()
bond_data['Return'] = bond_data['Adj Close'].pct_change()

# 年次リターンの計算
sp500_annual_return = sp500_data['Return'].resample('Y').apply(lambda x: (1 + x).prod() - 1)
bond_annual_return = bond_data['Return'].resample('Y').apply(lambda x: (1 + x).prod() - 1)

# 期待リターンとリスクの計算
sp500_mean_return = sp500_annual_return.mean()
bond_mean_return = bond_annual_return.mean()

sp500_risk = sp500_annual_return.std()
bond_risk = bond_annual_return.std()

# 無リスク利子率（適当に年0.5％と仮定）
risk_free_rate = 0.005

# シャープレシオの計算
sp500_sharpe_ratio = (sp500_mean_return - risk_free_rate) / sp500_risk
bond_sharpe_ratio = (bond_mean_return - risk_free_rate) / bond_risk

# 結果の表示
print("S&P500:")
print(f"Expected Return: {sp500_mean_return:.2%}")
print(f"Risk (Standard Deviation): {sp500_risk:.2%}")
print(f"Sharpe Ratio: {sp500_sharpe_ratio:.2f}")

print("\nUS Bonds:")
print(f"Expected Return: {bond_mean_return:.2%}")
print(f"Risk (Standard Deviation): {bond_risk:.2%}")
print(f"Sharpe Ratio: {bond_sharpe_ratio:.2f}")

# 累積リターンの計算
sp500_cumulative_return = (1 + sp500_data['Return']).cumprod()
bond_cumulative_return = (1 + bond_data['Return']).cumprod()

# グラフの作成
plt.figure(figsize=(14, 7))
plt.plot(sp500_cumulative_return.index, sp500_cumulative_return, label='S&P 500', color='blue')
plt.plot(bond_cumulative_return.index, bond_cumulative_return, label='US Bonds', color='red')
plt.xlabel('Time')
plt.ylabel('Cumulative Return')
plt.title('Cumulative Return of S&P 500 and US Bonds')
plt.legend()
plt.grid(True)
plt.show()