import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# 銘柄リスト
tickers = ['SPY', 'TLT', 'IAU']

# データ取得期間の設定
start_date = '2014-01-01'  # 30年前のデータ
end_date = '2024-01-01'

# データをダウンロード（調整後終値を使用することで、配当金再投資を考慮）
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# 日次リターンを計算
returns = data.pct_change()

# 累積リターンを計算（配当金再投資を考慮）
cumulative_returns = (1 + returns).cumprod() - 1

# ポートフォリオの比率
weights = np.array([0.55, 0.15, 0.30])

# ポートフォリオの累積リターンを計算
portfolio_returns = returns.dot(weights)
portfolio_cumulative_returns = (1 + portfolio_returns).cumprod() - 1

# チャートのプロット
plt.figure(figsize=(14, 8))
for ticker in tickers:
    plt.plot(cumulative_returns.index, cumulative_returns[ticker] * 100, label=ticker)

# ポートフォリオの累積リターンを追加
plt.plot(portfolio_cumulative_returns.index, portfolio_cumulative_returns * 100, label='Portfolio (55% SPY, 15% TLT, 30% IAU)', linestyle='--', color='black')

plt.title('SPY, TLT, IAU - Cumulative Returns with Portfolio (%)')
plt.xlabel('Date')
plt.ylabel('Cumulative Return (%)')
plt.legend()
plt.grid(True)
plt.show()
