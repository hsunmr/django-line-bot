import requests
import pandas as pd

res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")

df = pd.read_html(res.text)[0]

# 設定column名稱
df.columns = df.iloc[0]
# 刪除第一行
df = df.iloc[2:]

# df = df.set_index('有價證券代號及名稱')

df['stock_code'] = df['有價證券代號及名稱'].str.split(' ').str.get(0)
df['stock_name'] = df['有價證券代號及名稱'].str.split(' ').str.get(1)
# stock_code = []
# stock_name = []
# for code in df['有價證券代號及名稱']:
#     stock = code.split('　')
#     stock_code.append(stock[0])
#     stock_name.append(stock[1])

# df['stock_code'] = stock_code
# df['stock_name'] = stock_name

df.to_csv("midterm.csv")