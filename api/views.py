from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import JsonResponse
from api.utils.auth import MyAuthtication
from api.utils.throttle import *
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from iosjk import *
import json
from datetime import datetime, date, timedelta
from rest_framework import HTTP_HEADER_ENCODING
from django.http import HttpResponseRedirect, HttpResponse

def md5(user):
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    print(auth, 'auth000000')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
        print(auth, 'auth')
    return auth



class Authtication(BaseAuthentication):#为了规范来继承
    """正式的放在utils.auth中"""
    def authenticate(self, request):

        print('来道验证管道')

        token = request._request.GET('token')
        print(token,'1111111111')

        sql = f"SELECT `user` FROM `user_token` where token ='{token}'"
        print(sql)
        df = pd.read_sql(sql, engine)
        print(df)

        # 然后进行判断 如果匹配的内容不对
        if len(df) < 1:
            raise exceptions.AuthenticationFailed('用户认证失败111')
        # 在rest_framework 内部会给reqeust赋值，以供后续操作使用
        user = df.iloc[0][0]
        return (user, token)


    def authenticate_header(self, request):
        pass






class LoginView(APIView):
    # throttle_classes = [VisitThrottle_User, ]  # 访问频率控制

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        # 设置状态码
        print(request.POST)
        ret = {"state_code": 1000, "msg": None}
        # 判断异常
        try:
            # 原生_request改写request方法 获取前端表单里面的用户名
            username = request.POST.get('username')
            # username = request._request.GET.get('username')
            print('username=', username)
            # 获取前端表单里面的密码
            password = request.POST.get('password')
            # password = request._request.GET.get('password')
            print('password', password)
            # 用变量名obj 接收数据库里的信息并进行 前端表单与数据库的匹配
            # obj = models.UserInfo.objects.filter(username=username, password=password).first()
            sql = f"select * from user_info where user='{username}' and pwd='{password}'"
            print(sql)
            df = pd.read_sql(sql, engine)
            print(df)
            # 然后进行判断 如果匹配的内容不对
            if len(df) < 1:
                # 就发送状态码 1001
                ret["state_code"] = 1001
                # 用户名或者 密码错误
                ret["msg"] = "用户名或者密码错误"
            # 否则为登陆用户创建一个token
            token = md5(username)
            print(token)
            d = {'user': username, 'token': token}
            ddf = pd.DataFrame([d])
            print(ddf)
            to_sql('user_token', engine, ddf, type='update')
            # 存到数据库 存在就更新,不存在就创建
            # tt = int(time.time())
            # models.UserToken.objects.update_or_create(user=obj, defaults={"token": token, 'time': tt})

            # 发送状态码
            ret["token"] = token
            # 告知请求成功
            ret["msg"] = "请求成功"
        # 判断异常
        except Exception as e:
            # 发送状态码
            print(e)
            ret["state_code"] = 1002
            # 请求异常
            ret["msg"] = "请求异常"

        # return JsonResponse(ret)
        if ret['state_code'] == 1000:
            # return JsonResponse(ret)
            return redirect('/api/class2/page1/isday')
            # return render(request, 'class2.html')
            # print(token, '!@$$#!@$!@$!@!#@!#!@#')
            # return redirect('/api/class2/page1/isday', kwargs={'token': token})
            # return redirect(f'/api/class2/page1/isday/token={token}')




            pindex = 1
            print(pindex)
            day_type = 'isday'
            print(day_type, '~~~~~~~~~~')
            num = 50
            if pindex == 1:
                p_start = 0
            else:
                p_start = (pindex - 1) * num

            sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` GROUP  BY `user`  LIMIT {p_start}, {num};"
            df = pd.read_sql(sql1, engine)
            df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
            df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
            df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
            cc = df.values.tolist()
            return render(request, 'class2.html', {'class_list': cc})




        else:
            # return HttpResponseRedirect("https://bbs.csdn.net/topics/350114292")
            return render(request, 'login.html', {'msg': '账号密码错误'})


def GB_MB(num):
    if num < 1024:
        return str(int(num))+'KB'
    r_num = num/1024
    if r_num < 1024:
        return str(int(r_num))+'MB'
    else:
        g_num = int(r_num / 1024)

        if g_num < 1024:
            return str(g_num) + 'GB'
        return str(int(g_num / 1024)) + 'TB'




class ClassView(APIView):

    # authentication_classes = [Authtication, ]#身份验证

    def get(self, request, *args, **kwargs):
        ret = {'code': 0, 'data': None, "detail": "", "message": None}
        try:
            pindex = int(kwargs.get('page'))
            # print(pindex)
            day_type = kwargs.get('type')
            # print(day_type,'~~~~~~~~~~')

            user = kwargs.get('user')[4:]
            # print(user,'~~~~~~~~~~')
            num = int(kwargs.get('num')[3:])

            if num:
                print(num,'~~~~~~~~~~')

            else:
                num = 50
            if pindex ==1:
                p_start=0
            else:
                p_start = (pindex-1)*num

            if day_type =="isday":
                # sql1 = f"-- SELECT date,up_sum, downlink, uplink  FROM `tank_day` ORDER BY date DESC  LIMIT {p_start}, {num};"
                sql1 = f"SELECT  date, sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink,user FROM `tank_day` WHERE `user`='{user}' GROUP  BY `user`,date ORDER BY date  LIMIT {p_start}, {num};"
                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="isyesterday":
                tt = str(datetime.today()-timedelta(days=1))[0:10]
                print(tt)
                sqlpass = f"SELECT update_time, uplink+downlink as up_sum, downlink,uplink FROM `tank` \
                        WHERE date = '{tt}' ORDER BY update_time DESC  LIMIT {p_start}, {num};"

                sql1 = f"SELECT hour(update_time) as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='{user}' and date(update_time)='{tt}' \
                        group by date(update_time),hour(update_time) ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)+':00-'+str(x+1)+':00')
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                print(cc)
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)

            if day_type=="istoday":
                tt = str(datetime.today()-timedelta(days=0))[0:10]
                print(tt)
                sqlpass = f"SELECT update_time, uplink+downlink as up_sum, downlink, uplink FROM `tank` \
                        WHERE date = '{tt}' ORDER BY update_time DESC  LIMIT {p_start}, {num};"
                sql1 = f"SELECT hour(update_time) as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='{user}' and date(update_time)='{tt}' \
                        group by date(update_time),hour(update_time) ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)+':00-'+str(x+1)+':00')
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="isweek":
                now = datetime.now()
                # this_week_start = str(now - timedelta(days=now.weekday()))[0:10]
                # this_week_end = str(now + timedelta(days=6 - now.weekday()))[0:10]
                today = str(datetime.now())
                day_7 = str(now - timedelta(days=7))[0:10]
                # sql1 = f"SELECT date, uplink+downlink as up_sum,downlink, uplink, user FROM `tank_day` \
                #         WHERE date  BETWEEN '{this_week_start}' AND '{this_week_end}' and user='{user}' ORDER BY date  LIMIT {p_start}, {num};"
                sql1 = f"SELECT CONCAT(date(update_time),' ',HOUR(update_time),':00')  as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='tank' and date(update_time) BETWEEN '{day_7}' and  '{today}' \
                        group by CONCAT(date(update_time),' ',HOUR(update_time),':00')  ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)



            if day_type=="isyear":
                sqlpass = f"SELECT concat(year(date),if(month(date)>=10,'',0),month(date)) as date, SUM(up_sum) as up_sum, SUM(downlink) as downlink, sum(uplink) as uplink \
                     FROM `tank_day` GROUP BY concat(year(date),if(month(date)>=10,'',0),month(date)) ORDER BY date DESC LIMIT {p_start}, {num};"

                sql1 = f"SELECT concat(year(date),if(month(date)>=10,'',0),month(date)) as date, SUM(up_sum) as up_sum, SUM(downlink) as downlink, sum(uplink) as uplink, user  \
                        FROM `tank_day` WHERE `user`='{user}' GROUP BY concat(year(date),if(month(date)>=10,'',0),month(date))  ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)[0:4]+'-'+str(x)[-2:])
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type[0:5] =="iszdy":
                strat = day_type[5:15]
                end = day_type[15:25]
                print(strat, end)
                sqlpass = f"SELECT date, uplink, downlink,up_sum FROM `tank_day` where date between '{strat}' and  '{end}' ORDER BY date DESC  LIMIT {p_start}, {num};"

                sql1 = f"SELECT  date, sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink,user FROM `tank_day` WHERE `user`='{user}' and date between '{strat}' and  '{end}' GROUP BY `user`,date ORDER BY date  LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)
        except BaseException as e:
            print(e)
        ret['code'] = 400
        # ret['data'] = cc
        ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
        return HttpResponse(ret)



    def post(self, request, *args, **kwargs):
        pass


class Class2View(APIView):

    # authentication_classes = [Authtication, ]#身份验证

    def post(self, request, *args, **kwargs):
        ret = {'code': 0, 'data': None, "detail": "", "message": None}
        try:
            print('到post了')

            print(request.data)
            num = int(request.data['num'])
            pindex = int(request.data['page'])
            day_type = request.data['type']
            user = request.data['user']

            print(num, day_type, pindex)

            # pindex = int(kwargs.get('page'))
            # # print(pindex)
            # day_type = kwargs.get('type')
            # # print(day_type,'~~~~~~~~~~')
            #
            # user = kwargs.get('user')[4:]
            # # print(user,'~~~~~~~~~~')
            # num = int(kwargs.get('num')[3:])

            if num:
                print(num,'~~~~~~~~~~')

            else:
                num = 50
            if pindex ==1:
                p_start=0
            else:
                p_start = (pindex-1)*num

            if day_type =="day":
                # sql1 = f"-- SELECT date,up_sum, downlink, uplink  FROM `tank_day` ORDER BY date DESC  LIMIT {p_start}, {num};"
                sql1 = f"SELECT  date, sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink,user FROM `tank_day` WHERE `user`='{user}' GROUP  BY `user`,date ORDER BY date  LIMIT {p_start}, {num};"
                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="yesterday":
                tt = str(datetime.today()-timedelta(days=1))[0:10]
                print(tt)
                sqlpass = f"SELECT update_time, uplink+downlink as up_sum, downlink,uplink FROM `tank` \
                        WHERE date = '{tt}' ORDER BY update_time DESC  LIMIT {p_start}, {num};"

                sql1 = f"SELECT hour(update_time) as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='{user}' and date(update_time)='{tt}' \
                        group by date(update_time),hour(update_time) ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)+':00-'+str(x+1)+':00')
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                print(cc)
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)

            if day_type=="today":
                tt = str(datetime.today()-timedelta(days=0))[0:10]
                print(tt)
                sqlpass = f"SELECT update_time, uplink+downlink as up_sum, downlink, uplink FROM `tank` \
                        WHERE date = '{tt}' ORDER BY update_time DESC  LIMIT {p_start}, {num};"
                sql1 = f"SELECT hour(update_time) as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='{user}' and date(update_time)='{tt}' \
                        group by date(update_time),hour(update_time) ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)+':00-'+str(x+1)+':00')
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="week_hour":
                now = datetime.now()
                # this_week_start = str(now - timedelta(days=now.weekday()))[0:10]
                # this_week_end = str(now + timedelta(days=6 - now.weekday()))[0:10]
                today = str(datetime.now())
                day_7 = str(now - timedelta(days=7))[0:10]
                # sql1 = f"SELECT date, uplink+downlink as up_sum,downlink, uplink, user FROM `tank_day` \
                #         WHERE date  BETWEEN '{this_week_start}' AND '{this_week_end}' and user='{user}' ORDER BY date  LIMIT {p_start}, {num};"
                sql1 = f"SELECT CONCAT(date(update_time),' ',HOUR(update_time),':00')  as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='tank' and date(update_time) BETWEEN '{day_7}' and  '{today}' \
                        group by CONCAT(date(update_time),' ',HOUR(update_time),':00')  ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="week_day":
                now = datetime.now()
                today = str(datetime.now())
                day_7 = str(now - timedelta(days=7))[0:10]
                # sql1 = f"SELECT date, uplink+downlink as up_sum,downlink, uplink, user FROM `tank_day` \
                #         WHERE date  BETWEEN '{this_week_start}' AND '{this_week_end}' and user='{user}' ORDER BY date  LIMIT {p_start}, {num};"
                sql1 = f"SELECT CONCAT(date(update_time))  as date, sum(uplink+downlink) as up_sum, sum(downlink) as downlink, sum(uplink) as uplink, user \
                        FROM tank WHERE  user='tank' and date(update_time) BETWEEN '{day_7}' and  '{today}' \
                        group by CONCAT(date(update_time))  ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)



            if day_type=="year":
                sqlpass = f"SELECT concat(year(date),if(month(date)>=10,'',0),month(date)) as date, SUM(up_sum) as up_sum, SUM(downlink) as downlink, sum(uplink) as uplink \
                     FROM `tank_day` GROUP BY concat(year(date),if(month(date)>=10,'',0),month(date)) ORDER BY date DESC LIMIT {p_start}, {num};"

                sql1 = f"SELECT concat(year(date),if(month(date)>=10,'',0),month(date)) as date, SUM(up_sum) as up_sum, SUM(downlink) as downlink, sum(uplink) as uplink, user  \
                        FROM `tank_day` WHERE `user`='{user}' GROUP BY concat(year(date),if(month(date)>=10,'',0),month(date))  ORDER BY date LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x)[0:4]+'-'+str(x)[-2:])
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if type(day_type) == list:
                strat = day_type[0]
                end = day_type[1]
                print(strat, end)
                sqlpass = f"SELECT date, uplink, downlink,up_sum FROM `tank_day` where date between '{strat}' and  '{end}' ORDER BY date DESC  LIMIT {p_start}, {num};"

                sql1 = f"SELECT  date, sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink,user FROM `tank_day` WHERE `user`='{user}' and date between '{strat}' and  '{end}' GROUP BY `user`,date ORDER BY date  LIMIT {p_start}, {num};"

                df = pd.read_sql(sql1, engine)
                df['date'] = df['date'].apply(lambda x: str(x))
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)
        except BaseException as e:
            print(e)
        ret['code'] = 400
        # ret['data'] = cc
        ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
        return HttpResponse(ret)







class IndexView(APIView):

    # authentication_classes = [Authtication, ]#身份验证

    def get(self, request, *args, **kwargs):
        ret = {'code': 0, 'data': None, "detail": "", "message": None}
        pindex = int(kwargs.get('page'))
        print(pindex)
        day_type = kwargs.get('type')
        print(day_type, '~~~~~~~~~~')
        # num = 13
        num = int(kwargs.get('num')[3:])

        if num:
            print(num, '~~~~~~~~~~')

        else:
            num = 50
        if pindex == 1:
            p_start = 0
        else:
            p_start = (pindex - 1) * num

        try:
            if day_type == "isday":
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` GROUP  BY `user`  LIMIT {p_start}, {num};"
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="isyesterday":
                tt = str(datetime.today()-timedelta(days=1))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM  `tank_day` where date = '{tt}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)

            if day_type=="istoday":
                tt = str(datetime.today()-timedelta(days=0))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day`  where date = '{tt}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})

                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="isweek":
                now = datetime.now()
                this_week_start = str(now - timedelta(days=now.weekday()))[0:10]
                this_week_end = str(now + timedelta(days=6 - now.weekday()))[0:10]
                today = str(datetime.now())
                day_7 = str(now - timedelta(days=7))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` where date between '{day_7}' and '{today}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)



            if day_type=="isyear":
                tt = str(datetime.today()-timedelta(days=1))[0:4]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM  `tank_day` where date like '{tt}%%' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type[0:5] =="iszdy":
                #http://121.37.252.51:7070/api/class2/page1/iszdy2020-05-292020-06-07
                strat = day_type[5:15]
                end = day_type[15:25]

                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` where date between '{strat}' and '{end}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)
        except BaseException as e:
            ret['code'] = 400
            ret['message'] = str(e)
            print(ret)
        ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
        return HttpResponse(ret)


class Index2View(APIView):

    # authentication_classes = [Authtication, ]#身份验证

    def post(self, request, *args, **kwargs):
        ret = {'code': 0, 'data': None, "detail": "", "message": None}
        print('到post了')

        print(request.data)
        num = int(request.data['num'])
        pindex = int(request.data['page'])
        day_type = request.data['type']
        print(num,day_type,pindex)

        if num:
            print(num, '~~~~~~~~~~')

        else:
            num = 50
        if pindex == 1:
            p_start = 0
        else:
            p_start = (pindex - 1) * num

        try:
            if day_type == "day":
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` GROUP  BY `user`  LIMIT {p_start}, {num};"
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="yesterday":
                tt = str(datetime.today()-timedelta(days=1))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM  `tank_day` where date = '{tt}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)

            if day_type=="today":
                tt = str(datetime.today()-timedelta(days=0))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day`  where date = '{tt}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})

                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if day_type=="week":
                now = datetime.now()
                this_week_start = str(now - timedelta(days=now.weekday()))[0:10]
                this_week_end = str(now + timedelta(days=6 - now.weekday()))[0:10]
                today = str(datetime.now())
                day_7 = str(now - timedelta(days=7))[0:10]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` where date between '{day_7}' and '{today}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)



            if day_type=="year":
                tt = str(datetime.today()-timedelta(days=1))[0:4]
                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM  `tank_day` where date like '{tt}%%' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)


            if type(day_type) == list:
                #http://121.37.252.51:7070/api/class2/page1/iszdy2020-05-292020-06-07
                strat = day_type[0]
                end = day_type[1]

                sql1 = f"SELECT sum(up_sum) as up_sum, sum(downlink) as downlink, SUM(uplink) as uplink, user FROM `tank_day` where date between '{strat}' and '{end}' GROUP  BY `user`  LIMIT {p_start}, {num};"
                print(sql1)
                df = pd.read_sql(sql1, engine)
                df['uplink'] = df['uplink'].apply(lambda x: GB_MB(x))
                df['downlink'] = df['downlink'].apply(lambda x: GB_MB(x))
                df['up_sum'] = df['up_sum'].apply(lambda x: GB_MB(x))
                cc = df.values.tolist()
                # return render(request, 'class2.html', {'class_list': cc})
                ret['code'] = 200
                ret['data'] = cc
                ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
                return HttpResponse(ret)
        except BaseException as e:
            ret['code'] = 400
            ret['message'] = str(e)
            print(ret)
        ret = json.dumps(ret, ensure_ascii=False)  # ensure_ascii不做编码处理
        return HttpResponse(ret)






