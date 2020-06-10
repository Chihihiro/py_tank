# -*- coding: utf-8 -*-
# @Time    : 2020/5/25 13:51
# @Author  : Chihiro



from iosjk import *
from datetime import datetime, date, timedelta
os.chdir('/opt/py_tank/')
path = os.getcwd()

os.system("""./stat api --server=193.200.134.9:54322 StatsService.QueryStats 'pattern: "" reset: false'""")

time.sleep(4)



with open(path+'/v.log', 'r') as f:
    v = f.read()

# x = re.sub('\n','', v)

x2 = re.sub('>>>', '-', v)
all = x2.split('>')

up = []
down = []


for i in all:
    print(i)
    if 'user' not in i:
        pass
    else:
        user = re.search("user-(.+?)-traffic",i).group(1)
        value = re.search("value: (.+?)\n",i).group(1)
        if 'downlink' in i:
            up.append([user, value])
        else:
            down.append([user, value])




today = str(datetime.today().date())

df1 = pd.DataFrame(up)
df1.columns = ['user', 'uplink']
df2 = pd.DataFrame(down)
df2.columns = ['user', 'downlink']

df3 = pd.merge(df1, df2, how='inner')
df3['date'] = today
df3['uplink'] = df3['uplink'].apply(lambda x: int(x))
df3['downlink'] = df3['downlink'].apply(lambda x: int(x))
to_sql('tank', engine, df3, type="update")
#
#
#
import time
time.sleep(3)

now = datetime.now()
this_week_start = str(now - timedelta(days=now.weekday()))[:19]


sql = f"SELECT date,SUM(downlink) AS downlink, SUM(uplink) as uplink ,user, SUM(downlink+uplink) as up_sum FROM `tank` where update_time > '{this_week_start}' GROUP BY date, `user`"

df = pd.read_sql(sql, engine)
to_sql('tank_day', engine, df, type="update")


os.system(f'echo > {path+ "/v.log"}')


os.system("""./stat api --server=193.200.134.9:54322 StatsService.QueryStats 'pattern: "" reset: true'""")
