## PTT

import requests
from bs4 import BeautifulSoup

def get_all_href(url):
    output_dict = {}

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    

def ptt_crawler(topic):    
    # topic = 'Lifeismoney'
    content = ""
    url = 'https://www.ptt.cc/bbs/{}/index.html'.format(topic)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    results = soup.select("div.title")
    for item in results:
        item_a = item.select_one("a")
        title = item.text
        if item_a: # 判斷是否有被刪除的文章
            content += '{}{}\n\n'.format(title, 'https://www.ptt.cc'+ item_a.get('href'))
            # print(title, 'https://www.ptt.cc'+ item_a.get('href'))
            
    return content

content = ptt_crawler('Lifeismoney')
print(content)

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

# print(ptt_hot())

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


