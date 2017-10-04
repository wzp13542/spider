#encoding: utf-8

#pip install bs4
#做网页分析

#request
#pip install request
#做网络请求

#pip install lxml

# 第一步 把网页数据全部抓取下来      request
#第二部 把我抓取下来的数据进行过滤   bs4
#pip install echarts-python 数据可视化 百度开源的包
import requests
import time
from bs4 import BeautifulSoup
from echarts import Echart,Bar,Axis
import  json
TEMPERATURE_LIST = []
CITY_LIST = []
MIN_LIST = []
#get/post

def get_temperature(url):
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://www.weather.com.cn/textFC/hb.shtml',
        'Host': 'www.weather.com.cn'

    }

    req = requests.get(url, headers=headers)
    # 东北地区
    # 更换url 获取不同地区的信息
    """
    http://www.weather.com.cn/textFC/hb.shtml   华北
    http://www.weather.com.cn/textFC/db.shtml   东北
    http://www.weather.com.cn/textFC/hd.shtml   华东
    http://www.weather.com.cn/textFC/hz.shtml   华中
    http://www.weather.com.cn/textFC/hn.shtml   华南
    http://www.weather.com.cn/textFC/xb.shtml   西北   
    http://www.weather.com.cn/textFC/xn.shtml   西南
    http://www.weather.com.cn/textFC/gat.shtml  港澳台
    """
    content = req.content

    soup = BeautifulSoup(content, 'lxml')
    conMidtab = soup.find('div', class_='conMidtab')
    conMidtab2_list = conMidtab.find_all('div', class_='conMidtab2')
    for x in conMidtab2_list:
        tr_list = x.find_all('tr')[2:]
        province = ''
        for index, tr in enumerate(tr_list):
            min = 0
            max = 0
            if index == 0:
                td_list = tr.find_all('td')
                province = td_list[0].text.replace('\n', '')
                city = td_list[1].text.replace('\n', '')
                min = td_list[7].text.replace('\n', '')
                # max = td_list[4].text.replace('\n', '')
                # 暂时没有最高气温
            else:
                td_list = tr.find_all('td')
                city = td_list[0].text.replace('\n', '')
                min = td_list[6].text.replace('\n', '')
                # max = td_list[3].text.replace('\n', '')
                # 暂时没有最高气温

            #print '%s|%s' % (province + city, min)
            TEMPERATURE_LIST.append({
                'city': province+city,
                'min': min

            })
            CITY_LIST.append(province+city)
            MIN_LIST.append(min)

    """
        province_tr = tr_list[2]
        td_list = province_tr.find_all('td')
        province_td = td_list[0]
        province = province_td.text
        province1 = province.replace('\n','')
        print province1.replace('-','')
    """
    # for x in conMid_list:
    # print x
    # 所有城市都是放在属于某个省或者直辖市表格中


def main():
    urls = ["http://www.weather.com.cn/textFC/hb.shtml"]
    for url in urls:
        get_temperature(url)
        time.sleep(2)
    # 爬取页面 为了不爬崩页面 需要睡眠
    line = json.dumps(TEMPERATURE_LIST, ensure_ascii=False)
    # with open('temperature.json', 'w') as fp:
    #     fp.write(line.encode('utf-8'))

    #
    # with open('temperature.json','r') as fp:
    #     TEMPERATURE_LIST = json.load(fp,encoding='utf-8')

    SORTED_TEMPERATURE_LIST = sorted(TEMPERATURE_LIST, lambda x,y:cmp(int(x['min']),int(y['min'])))
    TOP20_TEMPERATURE_LIST = SORTED_TEMPERATURE_LIST[0:20]
    TOP20_CITY_LIST = []
    TOP20_MIN_LIST = []
    for city_min in TOP20_CITY_LIST:
        TOP20_CITY_LIST.append(city_min['city'])
        TOP20_MIN_LIST.append(city_min['min'])


    echart = Echart(u'全国最低温度排名', u'Osaikifu')
    #创建画布
    bar = Bar(u'最低温度', TOP20_MIN_LIST)
    axis = Axis('category','bottom', data=TOP20_CITY_LIST)
    #横纵坐标
    echart.use(bar)
    echart.use(axis)
    echart.plot()


if __name__=='__main__':
    main()


