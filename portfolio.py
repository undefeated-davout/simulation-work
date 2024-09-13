import yfinance as yf
import numpy as np
import pandas as pd

# ポートフォリオの銘柄とその比率
tickers = ['SPY', 'TLT', 'IAU']
weights = np.array([0.55, 0.15, 0.30])

# データを取得する期間
start_date = '2006-01-01'
end_date = '2024-01-01'

# データを取得
data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']

# 日次リターンを計算
returns = data.pct_change().dropna()

# 年次リターンとボラティリティの計算
annual_returns = returns.mean() * 252
annual_volatility = returns.std() * np.sqrt(252)

# ポートフォリオの期待年次リターンとボラティリティを計算
portfolio_return = np.dot(weights, annual_returns)
portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

# 無リスク利子率 (仮に0とする)
risk_free_rate = 0.0

# シャープレシオを計算
sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

# 結果を表示
print(f"Expected Annual Return: {portfolio_return:.2%}")
print(f"Expected Annual Volatility (Risk): {portfolio_volatility:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
