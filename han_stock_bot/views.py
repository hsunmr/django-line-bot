from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import csv
import requests

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# validate stock exist in csv file
def validate(search_input):
    with open('stocks.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        item = [stock for stock in rows if stock['code'] == search_input or stock['name'] == search_input]

        result = None
        if len(item) > 0:
            result = item[0]['search_code']

        return result

# call twse api to get info
def stock_info(search_input):

    search_code = validate(search_input)

    if search_code == None:
        return '沒有此代碼或名稱的股票，請確認後再查詢 :") 。'
    else:
        twse_url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={search_code}&json=1&delay=0'

        #call api
        result = (requests.get(twse_url)).json()

        result_message = '查無資料。'
        if len(result['msgArray']) > 0:
            msg = result['msgArray'][0]
            result_message = f'【{msg["n"]}】\n'
            result_message += f'當盤成交價:【{msg["z"]}】\n'
            result_message += f'開盤:【{msg["o"]}】\n'
            result_message += f'最高:【{msg["h"]}】\n'
            result_message += f'最低:【{msg["l"]}】\n'
            result_message += f'昨收:【{msg["y"]}】\n'
            result_message += f'累積成交量:【{msg["v"]}】\n'
            result_message += f'揭示買價:【{",".join((msg["b"].split("_"))[:5])}】\n'
            result_message += f'揭示賣價:【{",".join((msg["a"].split("_"))[:5])}】\n'

        return result_message

# code error
def code_error(search_input):
    return '您可以使用P加股票代碼或名稱。\n ex. P2330 or P台積電'

@csrf_exempt
def line_callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        switch = {'p' : stock_info}

        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                code = text[0].lower()
                search_input = text[1:]

                response = switch.get(code, code_error)(search_input)

                # reply
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=response)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
