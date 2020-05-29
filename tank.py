# -*- coding: utf-8 -*-
# @Time    : 2020/5/25 13:33
# @Author  : Chihiro

import os
os.chdir('/opt/py_tank/')

v = os.system("""./stat api --server=193.200.134.9:54322 StatsService.QueryStats 'pattern: "" reset: false'""")