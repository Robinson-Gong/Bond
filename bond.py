import numpy as np
import pandas as pd
import datetime
import math
import matplotlib.pyplot as plt
from matplotlib.pylab import style

df = pd.read_excel(r'C:\Users\Administrator\Desktop\data\债券\19恒大01.xlsx')


def realratio(R, B, i, n, d, S, r, N):
    if d <= 0:
        d = 0
    PV = R * B * (1 - math.pow(1 + i, -(n - 1)) + i * math.pow(1 + r, -d)) / i + (B - S) * math.pow(1 + r, -N)
    realratio = PV / S
    return realratio


df1 = pd.read_excel(r'C:\Users\Administrator\Downloads\中国国债收益率曲线历史数据.xlsx')
df1 = df1.sort_values('日期')
df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
df1['日期'] = pd.to_datetime(df1['日期'], format='%Y-%m-%d')
for i in range(df1.shape[0]):
    if df1.iloc[i, 0] < df.iloc[0, 0]:
        continue
    else:
        df1 = df1.iloc[i:, :]
        break
R = 0.072
B = 100
a = ['2019-05-06', '2020-05-06', '2021-05-06', '2022-05-06', '2023-05-05']
a = pd.to_datetime(a, format='%Y-%m-%d')
merged_df = pd.merge(df1, df, on='日期', how='left')
for i in range(merged_df.shape[0]):
    if np.isnan(merged_df.iloc[i, 5]):
        merged_df.iloc[i, 5] = merged_df.iloc[i - 1, 5]
    else:
        continue
    if np.isnan(merged_df.iloc[i, 4]):
        merged_df.iloc[i, 4] = merged_df.iloc[i - 1, 5]
    else:
        continue
    if np.isnan(merged_df.iloc[i, 6]):
        merged_df.iloc[i, 6] = 0.0
    else:
        continue
strike_date = datetime.datetime.strptime('2023-05-06', '%Y-%m-%d')
for i in range(merged_df.shape[0]):
    for j in range(len(a) - 1):
        if a[j] <= merged_df.iloc[i, 0] < a[j + 1]:
            merged_df.loc[i, 'n'] = len(a) - 1 - j
            merged_df.loc[i, 'd'] = (a[j + 1] - merged_df.iloc[i, 0]).days / 365
            merged_df.loc[i, 'N'] = (strike_date - merged_df.iloc[i, 0]).days / 365
        else:
            continue
for i in range(merged_df.shape[0]):
    n = merged_df.loc[i, 'n'] - 1
    d = merged_df.loc[i, 'd']
    N = merged_df.loc[i, 'N']
    I = merged_df.loc[i, '1年'] / 100
    S = merged_df.loc[i, '最低']
    r = merged_df.loc[i, '1年'] / 100
    merged_df.loc[i, 'profit'] = realratio(R, B, I, n, d, S, r, N) * 100
merged_df.iloc[:, 0] = pd.to_datetime(merged_df.iloc[:, 0], format='%Y-%m-%d')

style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('日期')
ax1.set_ylabel('实际利润率', color=color)
ax1.plot(merged_df['日期'], merged_df['profit'], 'r', merged_df['日期'], merged_df['profit'], '.r')
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('成交量', color=color)
ax2.plot(merged_df['日期'], merged_df['成交量'], 'b', merged_df['日期'], merged_df['成交量'], '.b')
fig.tight_layout()
plt.show()
