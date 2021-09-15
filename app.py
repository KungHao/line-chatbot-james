from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

## PTT

import requests
from bs4 import BeautifulSoup

ptt_list = ['Lifeismoney', 'Stock', 'Gossiping', 'Tech_Job', 'Beauty', 'Sex', 'e-shopping', 'japanavgirls', 'NSwitch', 'Shu-Lin']

def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content

#### PTT crawler

## 取得文章日期
def get_date(soup):
    date = soup.select('div.date')
    date_list = [x.text.strip() for x in date]
    return date_list

## 取上一頁
def get_up_url(soup):
    btn = soup.select('div.btn-group.btn-group-paging a')
    up_page_href = btn[1]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href
    return next_page_url

## 爬蟲
def ptt_crawler(topic, page=3):    
    # topic = 'Lifeismoney'
    output = ''
    url = 'https://www.ptt.cc/bbs/{}/index.html'.format(topic)
    load  = {
        'from': f'/bbs/{topic}/index.html',
        'yes': 'yes'
    }
    
    for _ in range(page):
        r = requests.get(url, cookies={'over18':'1'})
        soup = BeautifulSoup(r.text, 'html.parser')
        date_list = get_date(soup)
        results = soup.select("div.title")
        content = ""
        for idx, item in enumerate(results):
            item_a = item.select_one("a")
            title = item.text
            if item_a: # 判斷是否有被刪除的文章
                content += '{}{}{}\n\n'.format(date_list[idx], title, 'https://www.ptt.cc'+ item_a.get('href'))
                # print(title, 'https://www.ptt.cc'+ item_a.get('href'))
        output = content + output
        url = get_up_url(soup)
            
    return output

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content

def getConfig():
    import yaml
    path = './key.yaml'

    with open(path, 'r') as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except ValueError:
            print('INVALID YAML file format.. Please provide a good yaml file')
            exit(-1)

    return config['line_bot_api'], config['handler']

app = Flask(__name__)

LINE_BOT_API, HANDLER = getConfig()
line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # print("event.reply_token:", event.reply_token)
    # print("event.message.text:", event.message.text)
    if event.message.text.lower() == "hot":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif event.message.text in ptt_list:
        content = ptt_crawler(event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )
        return 0
    elif event.message.text == '科技新報':
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif event.message.text.lower() == 'show':
        flex_send_message = FlexSendMessage(
                alt_text='alt_text',
                contents={
                    'type':'bubble',
                    'header':{
                        'type':'box',
                        'layout':'vertical',
                        'contents':
                            [
                                {
                                    "type": "text",
                                    "text": "Choose one",
                                    "weight": "bold",
                                    "align": "center"
                                },
                                {
                                    "type": "separator",
                                    "color": "#000000",
                                    "margin": "xxl"
                                }
                            ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Lifeismoney",
                                    "text": "Lifeismoney"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Stock",
                                    "text": 'Stock'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Tech_Job",
                                    "text": 'Tech_Job'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "科技新報",
                                    "text": '科技新報'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Sex",
                                    "text": 'Sex'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "NSwitch",
                                    "text": 'NSwitch'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Beauty",
                                    "text": 'Beauty'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "japanavgirls",
                                    "text": 'japanavgirls'
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "Shu-Lin",
                                    "text": 'Shu-Lin'
                                }
                            }
                        ]
                    }
                }
            )
        
        line_bot_api.reply_message(event.reply_token, flex_send_message)
        
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
        return 0


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
