import json
from echarts import Echart,Bar,Axis


with open('temperature.json', 'r') as fp:
    TEMPERATURE_LIST = json.load(fp, encoding='utf-8')

SORTED_TEMPERATURE_LIST = sorted(TEMPERATURE_LIST, lambda x, y: cmp(int(x['min']), int(y['min'])))
TOP20_TEMPERATURE_LIST = SORTED_TEMPERATURE_LIST[0:20]
TOP20_CITY_LIST = []
TOP20_MIN_LIST = []
for city_min in TOP20_CITY_LIST:
    TOP20_CITY_LIST.append(city_min['city'])
    TOP20_MIN_LIST.append(city_min['min'])

echart = Echart(u'全国最低温度排名', u'Osaikifu')
# 创建画布
bar = Bar(u'最低温度', TOP20_MIN_LIST)
axis = Axis('category', 'bottom', data=TOP20_CITY_LIST)
# 横纵坐标
echart.use(bar)
echart.use(axis)
echart.plot()