# -*- coding: utf-8 -*-
# @Time    : 2020/5/25 13:51
# @Author  : Chihiro



from iosjk import *
from datetime import datetime, date, timedelta
os.chdir('/opt/py_tank/')
path = os.getcwd()

with open(path+'/v.log', 'r') as f:
    v = f.read()



downlink = re.search('name: "user>>>tank>>>traffic>>>downlink"\n  value: (.+?)\n>',v).group(1)
uplink = re.search('name: "user>>>tank>>>traffic>>>uplink"\n  value: (.+?)\n>',v).group(1)

print(downlink,uplink)



today = str(datetime.today().date())
df = pd.DataFrame([{'date': today, 'uplink': int(uplink), 'downlink': int(downlink)}])
to_sql('tank', engine, df, type="update")

import time
time.sleep(3)

now = datetime.now()
this_week_start = str(now - timedelta(days=now.weekday()))[:19]


# sql2 = "select d1.date, tank.uplink, tank.downlink,tank.uplink+tank.downlink as up_sum FROM ( \
# SELECT date,max(update_time) AS time FROM `tank`  GROUP BY date ) as d1 \
# JOIN tank ON d1.date = tank.date and d1.time =tank.update_time ORDER BY date DESC "
#

sql = f"SELECT date,SUM(downlink) AS downlink, SUM(uplink) as uplink ,user, SUM(downlink+uplink) as up_sum FROM `tank` where update_time > '{this_week_start}' GROUP BY date, `user`"

df = pd.read_sql(sql, engine)
to_sql('tank_day', engine, df, type="update")


os.system(f'echo > {path+ "/v.log"}')
