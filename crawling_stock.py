import requests
import pandas as pd
import csv

stock_info = [
    {
        'type' : 'tse',
        'url'  : 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    },
    {
        'type' : 'otc',
        'url'  : 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    }
]

def fetch_stock_data():

    stocks = [
        ['search_code', 'code', 'name']
    ]
    for item in stock_info:

        res = requests.get(item["url"])

        df = pd.read_html(res.text)[0]

        # 設定column名稱
        df.columns = df.iloc[0]

        for index, row in df.iterrows():
            stock = (row['有價證券代號及名稱']).split('　')
            if len(stock) > 1:
                stocks.append([f'{item["type"]}_{stock[0]}.tw', stock[0], stock[1]])

    with open('stocks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stocks)

if __name__ == '__main__':
    fetch_stock_data()


# search = '2330'
# with open('stocks.csv', newline='') as csvfile:

#     # 讀取 CSV 檔案內容
#     rows = csv.DictReader(csvfile)

#     a = [stock for stock in rows if stock['code'] == search or stock['name'] == search]

#     print(a[0]['search_code'])