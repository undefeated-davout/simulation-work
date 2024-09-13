import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データのダウンロード
start_date = '2000-01-01'
# start_date = '2018-01-01'
end_date = '2020-05-31'

sp500_data = yf.download('^GSPC', start=start_date, end=end_date, interval='1mo')
# bond_data = yf.download('IAU', start=start_date, end=end_date, interval='1mo')
bond_data = yf.download('^TNX', start=start_date, end=end_date, interval='1mo')

# リターンの計算
sp500_data['Return'] = sp500_data['Adj Close'].pct_change()
bond_data['Return'] = bond_data['Adj Close'].pct_change()

# 初期設定
monthly_investment = 300000  # 毎月の投資額

# ポートフォリオシミュレーション
def portfolio_simulation(strategy):
    balance_sp500 = 0
    balance_bond = 0
    balance_money = 0
    balance_total = [balance_sp500 + balance_bond]
    rate = 0.7

    sp = 0
    bnd = 0

    for i in range(1, len(sp500_data)):
        sp500_return = sp500_data['Return'].iloc[i]
        bond_return = bond_data['Return'].iloc[i]

        # リターン適用後の残高
        balance_sp500 *= (1 + sp500_return)
        balance_bond *= (1 + bond_return)

        if strategy == 'rebalance':
            # 6:4に近づくようにmonthly_investmentを使ってリバランス
            total_balance = balance_sp500 + balance_bond
            target_sp500 = total_balance * rate
            target_bond = total_balance * (1 - rate)

            if balance_sp500 < target_sp500:
                invest_sp500 = min(monthly_investment, target_sp500 - balance_sp500)
                balance_sp500 += invest_sp500
                balance_bond += monthly_investment - invest_sp500
            else:
                invest_bond = min(monthly_investment, target_bond - balance_bond)
                balance_bond += invest_bond
                balance_sp500 += monthly_investment - invest_bond


        elif strategy == 'rotation':
            # 毎月ローテーション（1〜11月）
            # if i % 12 != 11:
            if i % 36 != 35:
            # if True:
                if sp500_return > bond_return:
                  balance_sp500 += monthly_investment
                  # print('SP')
                  sp += 1
                else:
                  balance_bond += monthly_investment
                  # print('BND')
                  bnd += 1
                # print(f'sp500_return: {sp500_return} bond_return: {bond_return} balance_sp500: {balance_sp500} balance_bond: {balance_bond}')
            else:
                # 12月は6:4にリバランス
                total_balance = balance_sp500 + balance_bond
                total_balance += monthly_investment
                balance_sp500 = total_balance * rate
                balance_bond = total_balance * (1 - rate)

        elif strategy == 'sp500_only':
            balance_sp500 += monthly_investment

        elif strategy == 'bond_only':
            balance_bond += monthly_investment

        elif strategy == 'money':
            balance_money += monthly_investment
            balance_sp500 = balance_money
            balance_bond = 0

        balance_total.append(balance_sp500 + balance_bond)
    
    print(f'SP: {sp}, BND: {bnd}')

    return balance_total

# 各戦略のシミュレーション実行
sp500_only_balance = portfolio_simulation('sp500_only')
bond_only_balance = portfolio_simulation('bond_only')
rebalance_balance = portfolio_simulation('rebalance')
rotation_balance = portfolio_simulation('rotation')
money_balance = portfolio_simulation('money')

# グラフの作成
plt.figure(figsize=(14, 7))
plt.plot(sp500_data.index, sp500_only_balance, label='S&P 500 Only', color='blue')
plt.plot(bond_data.index, bond_only_balance, label='US Bonds Only', color='red')
plt.plot(sp500_data.index, rebalance_balance, label='Rebalance Strategy', color='green')
plt.plot(sp500_data.index, rotation_balance, label='Rotation Strategy', color='orange')
plt.plot(sp500_data.index, money_balance, label='money', color='orange')

plt.xlabel('Time')
plt.ylabel('Portfolio Value (JPY)')
plt.title('Portfolio Simulation: S&P 500 vs US Bonds vs Rebalance vs Rotation')
plt.legend()
plt.grid(True)
plt.show()