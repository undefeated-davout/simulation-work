import yfinance as yf
import numpy as np
from scipy.optimize import minimize

# 銘柄リスト
tickers = ['SPY', 'TLT', 'IAU']

# データ取得期間の設定
start_date = '2006-01-01'  # データの開始日
end_date = '2024-01-01'    # データの終了日

# データをダウンロード（調整後終値を使用）
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# 日次リターンを計算
returns = data.pct_change()

# 月次リターンを計算
monthly_returns = returns.resample('ME').apply(lambda x: (1 + x).prod() - 1)

# 年率リターンと年率ボラティリティを計算する関数
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 12
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(12)
    return returns, std

# シャープレシオを最大化するための目的関数
def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
    p_returns, p_std = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_returns - risk_free_rate) / p_std  # シャープレシオを負にして最小化

# 制約条件: 各資産の比率の合計が1になること
def check_sum(weights):
    return np.sum(weights) - 1

# 初期の資産比率
num_assets = len(tickers)
initial_weights = np.array([1.0 / num_assets] * num_assets)

# 平均リターンと共分散行列の計算
mean_returns = monthly_returns.mean()
cov_matrix = monthly_returns.cov()

# 最適化の実行
constraints = ({'type': 'eq', 'fun': check_sum})
bounds = tuple((0, 1) for asset in range(num_assets))
optimized = minimize(negative_sharpe_ratio, initial_weights, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

# 最適な比率
optimal_weights = optimized.x

# 最適なシャープレシオとパフォーマンス
optimal_returns, optimal_std = portfolio_performance(optimal_weights, mean_returns, cov_matrix)
optimal_sharpe_ratio = optimal_returns / optimal_std

# 指定された比率（SPY: 55%、TLT: 15%、IAU: 30%）の成績を計算
specified_weights = np.array([0.55, 0.15, 0.30])
specified_returns, specified_std = portfolio_performance(specified_weights, mean_returns, cov_matrix)
specified_sharpe_ratio = specified_returns / specified_std

# 結果の表示
print("Optimal Portfolio Weights:")
for i, ticker in enumerate(tickers):
    print(f"{ticker}: {optimal_weights[i]:.2%}")

print(f"\nOptimal Portfolio Performance:")
print(f"Expected Annual Return: {optimal_returns:.2%}")
print(f"Expected Annual Volatility (Risk): {optimal_std:.2%}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.2f}")

print("\nSpecified Portfolio Weights (SPY: 55%, TLT: 15%, IAU: 30%):")
print(f"SPY: 55.00%")
print(f"TLT: 15.00%")
print(f"IAU: 30.00%")

print(f"\nSpecified Portfolio Performance:")
print(f"Expected Annual Return: {specified_returns:.2%}")
print(f"Expected Annual Volatility (Risk): {specified_std:.2%}")
print(f"Sharpe Ratio: {specified_sharpe_ratio:.2f}")
