from pymongo import MongoClient
from flask import Flask,render_template,flash,request,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,current_user,login_required
import requests
import certifi
import json
import re
import datetime
import time
from bs4 import BeautifulSoup
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import tok,mongo,s_key,p,token_berdoff
import random
import testip


cluster=MongoClient(mongo,tlsCAFile=certifi.where())
db=cluster["UsersData"]
collection=db["forms"]
loggs=db["logs"]
rakbots=db["RAKBOT"]
rakbots_dostup=db["RAKBOT_DOSTUP"]

SECRET_KEY=s_key
app = Flask(__name__,static_folder="static")
app.secret_key=SECRET_KEY


def norm_money(money):
    money=list(str(money))
    for i in range(len(money),0,-3):
        money.insert(i,".")
    money=money[:-1]
    return "".join(money)

def get_int_time(time):
    return int(int(time.split(":")[0]))*3600+int(time.split(":")[1])*60+int(time.split(":")[2])

def get_normal_time(time):
    hours=str(time//3600)
    if len(hours)<2:
        hours="0"+hours
    minutes=str(time%3600//60)
    if len(minutes)<2:
        minutes="0"+minutes
    seconds=str(time%60)
    if len(seconds)<2:
        seconds="0"+seconds
    return (hours+":"+minutes+":"+seconds)


def get_token(a):
    token=a.text.split("\"csrf-token\" content=\"")[1].split("\">")[0]
    return token

id_be=16
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}


def chat_sender(text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                print(b)
                vk_session.method('messages.send', {'chat_id': id_be, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'chat_id': id_be, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'chat_id': id_be, 'message': text, 'disable_mentions': 1, 'random_id': 0})


def send_to_user(idd,text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                vk_session.method('messages.send', {'user_id': idd, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'user_id': idd, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'user_id': idd, 'message': text, 'disable_mentions': 1, 'random_id': 0})


vk_session = vk_api.VkApi(token = tok)
longpoll = VkBotLongPoll(vk_session,212957523)





@app.route("/")
def main():
    return "Test message<br><br><br><br><br><br>-,kz<br>©berdoff corp"

@app.route("/api/authlogs",methods=["GET","POST"])
def delll():
    global logs
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
    if request.method=="GET" or request.method=="POST":
        code=request.form.get("code")
        sess = requests.session()
        a=sess.get("https://arizonarp.logsparser.info/login")
        token=get_token(a)
        print(token)
        a=sess.post("https://arizonarp.logsparser.info/login",data={"name":"Lorenzo_Almas","password":{p},"_token":token})
        token=get_token(a)
        print(token)
        
        a=sess.post("https://arizonarp.logsparser.info/authenticator",data={"_token":token,"code":code},headers=header)
        if "Queen-Creek" in a.text:
            loggs.update_one({"type":"token"},{"$set":{"session":str(a.cookies["laravel_session"])}})
            return "Вошло"
        else:
            return "Не вошло"+" "+get_token(a)+" "+code+"\n"

@app.route("/checklogs",methods=["GET","POST"])
def dwadwadwa():
    global logs
    if request.method=="GET" or request.method=="POST":
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
        sess = requests.session()
        xsrf=loggs.find_one({"type":"token"})["session"]
        sess.headers.update(header)
        sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf,"_token":"BQoKlviexTmz612jcCTHz5xzJn4d3KLyBXEYDa97"})
        a=sess.get("https://arizonarp.logsparser.info/")
        if "Queen-Creek" in a.text:
            return BeautifulSoup(a.text,"lxml").find("a",class_="nav-link dropdown-toggle").text
        else:
            return "-\n\n"+xsrf

@app.route("/loadlogsdawdawdwadwadwadwadwa2121",methods=["GET","POST"])
def load_7days():
    global logs
    if request.method=="GET" or request.method=="POST":
        nick=request.form.get("nick")
        token=request.form.get("token")
        server=request.form.get("server")
        print("1")
        if token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"]
            sess.headers.update(header)
            sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf,"_token":"BQoKlviexTmz612jcCTHz5xzJn4d3KLyBXEYDa97"})
            a="Queen-Creek"
            if "Queen-Creek" in a:
                date = datetime.datetime.now()+datetime.timedelta(days=1)
                year_today = date.year
                if len(str(date.month)) == 1:
                    month_today = "0" + str(date.month)
                else:
                    month_today = str(date.month)
                if len(str(date.day)) == 1:
                    day_today = "0" + str(date.day)
                else:
                    day_today = str(date.day)
                date = date - datetime.timedelta(days=8)
                year = str(date.year)
                if len(str(date.month)) == 1:
                    month = "0" + str(date.month)
                else:
                    month = str(date.month)
                if len(str(date.day)) == 1:
                    day = "0" + str(date.day)
                else:
                    day = str(date.day)
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=login&sort=desc&player={nick}")
                logs=BeautifulSoup(logs.text,"lxml")
                stroka=logs.find_all("tr")[1]
                reg_ip = stroka.find_all("span", class_="badge badge-primary")[0].text
                last_ip = stroka.find_all("span", class_="badge badge-secondary")[0].text
                last_info = testip.get_info_by_ip(last_ip)
                last_city = last_info["city"]
                last_region = last_info["region"]
                reg_info = testip.get_info_by_ip(reg_ip)
                reg_city = reg_info["city"]
                reg_region = reg_info["region"]
                nick=stroka.text.split()[3]
                last_auth=stroka.text.split()[0]+" "+stroka.text.split()[1]
                id_acc=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[0].find("code").text
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=login&type%5B%5D=disconnect&sort=desc&player={id_acc}")
                logs=BeautifulSoup(logs.text,"lxml")
                stroka=logs.find_all("tr")[1:]
                for i in stroka:
                    if "авторизация: Есть" in i.text or "авторизовался" in i.text:
                        stroka=i
                        break
                nick=stroka.text.split()[3]
                vc_money=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[1].find("code").text
                lich1_money=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[2].find("code").text
                lich2_money=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[3].find("code").text
                lich3_money=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[4].find("code").text
                deposit=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[5].find("code").text
                if lich1_money=="4,294,967,295":
                    lich1_money="0"
                if lich2_money=="4,294,967,295":
                    lich2_money="0"
                if lich3_money=="4,294,967,295":
                    lich3_money="0"
                money_nal=stroka.find_all("code")[1].text
                money_bank=stroka.find_all("code")[2].text
                donate=stroka.find_all("code")[3].text
                money_all=norm_money(int(money_nal.replace(",",""))+int(money_bank.replace(",",""))+int(deposit.replace(",",""))+int(lich1_money.replace(",",""))+int(lich2_money.replace(",",""))+int(lich3_money.replace(",","")))
                lvl_adm=stroka.find_all("div",class_="app__hidden")[0].find_all("li")[6].find("code").text
                if lvl_adm!="0":
                    lvl_adm="Уровень адм: "+lvl_adm+"<br>"
                else:
                    lvl_adm=""

                try:
                    ban=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=ban&type%5B%5D=unban&sort=desc&player={nick}")
                    logs=BeautifulSoup(ban.text,"lxml")
                    stroki=logs.find_all("tr")[1]
                    if "забанил" in stroki.text:
                        if stroki.text.split()[6]==nick:
                            day=int(stroki.text.split()[8])
                            last_ban=datetime.datetime.strptime(stroki.text.split()[0]+" "+stroki.text.split()[1], '%Y-%m-%d %H:%M:%S')
                            last_ban=int(str(time.mktime(last_ban.timetuple())).split(".")[0])
                            now_time=int(str(time.time()).split(".")[0])+10800
                            if (now_time-int(last_ban))<(day*86400):
                                bban=" ".join(stroki.text.split("I:")[0].strip().split())
                                prichina=bban.split("причина: ")[1]
                                ban_do=str(datetime.datetime.utcfromtimestamp(int(last_ban)+(day*86400)).strftime('%Y-%m-%d %H:%M:%S'))
                                bban=f"<br>⛔Забанен за {prichina}⛔<br>Забанил: "+bban.split()[3]+"<br>Дата блокировки: "+stroki.text.split()[0]+" "+stroki.text.split()[1]+f"<br>Бан до {ban_do}"
                            else:
                                bban="✅ Аккаунт не заблокирован"
                        else:
                            bban="✅ Аккаунт не заблокирован"
                    else:
                        bban="✅ Аккаунт не заблокирован"
                except:
                    bban="✅ Аккаунт не заблокирован"
                strr=[]
                k=1
                print(k)
                url=""
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year}-{month}-{day}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                while "Игрок" in logs.text or "Администратор" in logs.text:
                    print(k)
                    logs=BeautifulSoup(logs.text,"lxml")
                    stroka=logs.find_all("tr")[1:]
                    for i in stroka:
                        if "авторизовался" in i.text or "авторизация: Есть" in i.text:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split())+" [R-IP: "+i.find_all("span", class_="badge badge-primary")[0].text+" L-IP: "+i.find_all("span", class_="badge badge-secondary")[0].text+"]")
                        else:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split()))
                    k+=1
                    logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year}-{month}-{day}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                    
                for i in range(18):
                    url+=random.choice("ASGVODWUIQPOXIMHWAPOIMdjopawicpmha1235432179796")
                f=open(f"logs/{url}.txt","w")
                f.write(f"Ник: {nick}[{id_acc}] Server: [{server}]<br>{lvl_adm}Az-Coin: {donate}<br>На руках: {money_nal}$<br>Банк: {money_bank}$<br>Депозит: {deposit}$<br>VC: {vc_money}$<br>Личный счет №1: {lich1_money}$<br>Личный счет №2: {lich2_money}$<br>Личный счет №3: {lich3_money}$<br>Всего денег: {money_all}$<br>Последний вход: {last_auth}<br>R-IP: {reg_ip} [{reg_city},{reg_region}]<br>L-IP: {last_ip} [{last_city},{last_region}]<br>{bban}<br><br><br>"+"<br>".join(strr))
                f.close()
                return url
            else:
                return "-"
        else:
            return "Access denied"

@app.route("/getlogs",methods=["GET","POST"])
def get_7days():
    global logs
    if request.method=="GET" or request.method=="POST":
        token=request.args.get('token')
        print(token)
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
        try:
            f=open(f"logs/{token}.txt","r")
            return f.readline()
        except:
            return "Ошибка"


@app.route("/getonline",methods=["GET","POST"])
def getonl():
    server="21"
    if request.method=="GET" or request.method=="POST":
        token = request.form.get("token")
        nick = request.form.get("nick")
        server=request.form.get("server")
        print(nick,token)
        if token == token_berdoff:
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf = loggs.find_one({"type": "token"})["session"]
            sess.headers.update(header)
            sess.cookies.update({"laravel_session": xsrf, "XSRF-TOKEN": xsrf, "_token": "BQoKlviexTmz612jcCTHz5xzJn4d3KLyBXEYDa97"})
            a = sess.get("https://arizonarp.logsparser.info/")
            if "Queen-Creek" in a.text:
                date = datetime.datetime.now()+datetime.timedelta(days=1)
                year_today = date.year
                if len(str(date.month)) == 1:
                    month_today = "0" + str(date.month)
                else:
                    month_today = str(date.month)
                if len(str(date.day)) == 1:
                    day_today = "0" + str(date.day)
                else:
                    day_today = str(date.day)
                date = date - datetime.timedelta(days=15)
                year = str(date.year)
                if len(str(date.month)) == 1:
                    month = "0" + str(date.month)
                else:
                    month = str(date.month)
                if len(str(date.day)) == 1:
                    day = "0" + str(date.day)
                else:
                    day = str(date.day)
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=login&type%5B%5D=disconnect&sort=desc&min_period={year}-{month}-{day}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={nick}&limit=1000")
                logs = BeautifulSoup(logs.text, "lxml")
                stroki = logs.find_all("tr")[1:]
                online={"online":{},"reports":{}}
                try:
                    i=stroki[0]
                    i = " ".join(i.text.split("I:")[0].strip().split())
                    dday=i.split()[0]
                    ctime=0
                    gtime=0
                    
                    if "авторизовался" in i:
                        date = datetime.datetime.now()-datetime.datetime.strptime(i.split()[0]+" "+i.split()[1], '%Y-%m-%d %H:%M:%S')
                        date=datetime.datetime.strptime(str(date).split(".")[0], '%H:%M:%S')
                        data=str(date.hour)+":"+str(date.minute)+":"+str(date.second)
                        ctime+=get_int_time(data)
                    for i in stroki:
                        i = " ".join(i.text.split("I:")[0].strip().split())
                        if "Есть" in i:
                            if dday==i.split()[0]:
                                if get_int_time(i.split()[1])<get_int_time(i.split("сессии:")[1].split(",")[0]):
                                    print(str(i.split()[1]),str(i.split("сессии:")[1].split(",")[0]))
                                    ctime+=get_int_time(i.split()[1])
                                    gtime=get_int_time(i.split("сессии:")[1].split(",")[0])-get_int_time(i.split()[1])
                                else:
                                    gtime=0
                                    ctime+=get_int_time(i.split("сессии:")[1].split(",")[0])
                            else:
                                online["online"][dday]=get_normal_time(ctime)
                                ctime=0
                                ctime+=gtime
                                gtime=0
                                dday=i.split()[0]
                                if get_int_time(i.split()[1]) < get_int_time(i.split("сессии:")[1].split(",")[0]):
                                    print(str(i.split()[1]), str(i.split("сессии:")[1].split(",")[0]))
                                    ctime += get_int_time(i.split()[1])
                                    gtime = get_int_time(i.split("сессии:")[1].split(",")[0]) - get_int_time(i.split()[1])
                                else:
                                    gtime = 0
                                    ctime += get_int_time(i.split("сессии:")[1].split(",")[0])
                    
                    k=1
                except:
                    pass
                try:
                    reports=0
                    date = datetime.datetime.now()+datetime.timedelta(days=1)
                    for i in range(15):
                        date=date-datetime.timedelta(days=1)
                        dd=""
                        dd+=str(date.year)+"-"
                        if len(str(date.month)) == 1:
                            dd += "0" + str(date.month)+"-"
                        else:
                            dd += str(date.month)+"-"
                        if len(str(date.day)) == 1:
                            dd += "0" + str(date.day)
                        else:
                            dd += str(date.day)
                    
                        online["reports"][dd]=0
                    logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=report_answer&sort=desc&min_period={year}-{month}-{day}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={nick}&limit=1000&page={k}")
                    logs = BeautifulSoup(logs.text, "lxml")
                    logs=logs.find("table",class_="table table-hover")
                    while "ответил на репорт" in logs.text:
                        for i in online["reports"]:
                            online["reports"][i]=online["reports"][i]+logs.text.count(i)
                        print(k)        
                        k+=1
                        logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&type%5B%5D=report_answer&sort=desc&min_period={year}-{month}-{day}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={nick}&limit=1000&page={k}")
                        logs = BeautifulSoup(logs.text, "lxml")
                        logs=logs.find("table",class_="table table-hover")
                except:
                    pass
                return online

            else:
                return {"status": "ne ok", "reason": "Логи не авторизованы"}


@app.route("/api/getpunish",methods=["GET","POST"])
def get_punish():
    if request.method=="GET" or request.method=="POST":
        token=request.form.get("token")
        nick=request.form.get("nick")
        if token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"]
            sess.headers.update(header)
            sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf,"_token":"BQoKlviexTmz612jcCTHz5xzJn4d3KLyBXEYDa97"})
            a=sess.get("https://arizonarp.logsparser.info/")
            if "Queen-Creek" in a.text:
                return sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B%5D=rmute&type%5B%5D=unrmute&type%5B%5D=skick&type%5B%5D=weap&type%5B%5D=spawnplayer&type%5B%5D=ban&type%5B%5D=jail&type%5B%5D=kick&type%5B%5D=mute&type%5B%5D=uval&type%5B%5D=warn&type%5B%5D=banip&type%5B%5D=unban&type%5B%5D=unjail&type%5B%5D=unmute&type%5B%5D=unwarn&type%5B%5D=unwarn_talon&sort=desc&player={nick}").text
            else:
                return {"status":"ne ok","reason":"Логи не авторизованы"}


@app.route("/api/getrakbot",methods=["GET","POST"])
def get_rakbot():
    if request.method=="GET" or request.method=="POST":
        rks=[]
        for i in rakbots.find():
            rks.append({"vk":i["vk"],"nick":i["nick"],"IP":i["IP"]})
            ttime=i["time"]
            if int(time.time())-int(ttime)>180:
                rakbots.delete_one({"vk":i["vk"],"time":ttime})
        return rks


@app.route("/api/addrakbot",methods=["GET","POST"])
def add_rakbot():
    if request.method=="GET" or request.method=="POST":
        nick=request.form.get("nick")
        ip=request.form.get("ip")
        tttime=int(time.time())
        vk=request.form.get("vk")
        if rakbots.count_documents({"nick":nick})==0:
            rakbots.insert_one({"nick":nick,"vk":vk,"IP":ip,"time":tttime})
        else:
            rakbots.delete_many({"nick":nick})
            rakbots.insert_one({"nick":nick,"vk":vk,"IP":ip,"time":tttime})

@app.route("/api/dellrakbot",methods=["GET","POST"])
def dell_rakbot():
    if request.method=="GET" or request.method=="POST":
        nick=request.args.get("nick")

        rakbots.delete_one({"nick":nick})

        try:
            vk=rakbots_dostup.find_one({"nick":nick})["vk"]
            send_to_user(vk,f"Ракбот успешно снят {nick}")
        except:
            chat_sender(f"Ракбот успешно снят {nick}")
        return "True"


@app.route("/api/getjoin",methods=["GET","POST"])
def get_join():
    if request.method=="GET" or request.method=="POST":
        token=request.form.get("token")
        pages=1
        if token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"]
            sess.headers.update(header)
            sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf,"_token":"BQoKlviexTmz612jcCTHz5xzJn4d3KLyBXEYDa97"})
            a=sess.get("https://arizonarp.logsparser.info/")
            if "Queen-Creek" in a.text:
                print("Вошло")
                date=datetime.datetime.now()
                year_today=date.year
                if len(str(date.month))==1:
                    month_today="0"+str(date.month)
                else:
                    month_today=str(date.month)
                if len(str(date.day))==1:
                    day_today="0"+str(date.day)
                else:
                    day_today=str(date.day)
                date=date-datetime.timedelta(days=1)
                year=str(date.year)
                if len(str(date.month))==1:
                    month="0"+str(date.month)
                else:
                    month=str(date.month)
                if len(str(date.day))==1:
                    day="0"+str(date.day)
                else:
                    day=str(date.day)
                joins=[]
                a=sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B0%5D=login&sort=desc&min_period={year}-{month}-{day}%2000%3A00%3A00&max_period={year_today}-{month_today}-{day_today}%2000%3A00%3A00&limit=1000&page={pages}")
                while "авторизовался" in a.text:
                    pages+=1
                    joins.append(a.text)
                    a=sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B0%5D=login&sort=desc&min_period={year}-{month}-{day}%2000%3A00%3A00&max_period={year_today}-{month_today}-{day_today}%2000%3A00%3A00&limit=1000&page={pages}")
                return {"status":"ok","text":joins}
            else:
                return {"status":"ne ok","reason":"Логи не авторизованы"}

@app.route("/api/forms",methods=["GET","POST"])
def go_form():
    if request.method == "GET" or request.method == "POST":
        token=request.args.get("token")
        check=request.args.get("check")
        #if token=="321321dwadwad21" and check=="1":
        a=collection.find({"status":0})
        if token==token_berdoff:
            forms=[]
            for i in a:
                forms.append(i["forma"])
                collection.update_one(i,{"$set":{"status":1}})
            return json.dumps(forms)

@app.route("/api/forms_plus",methods=["GET","POST"])
def forms_plus():
    if request.method == "GET" or request.method == "POST":
        """
        sess=requests.session()
        xsrf=loggs.find_one({"type":"token"})["session"]
        sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf})
        date=datetime.datetime.now()
        date=date-datetime.timedelta(minutes=1)
        year=date.year
        if len(str(date.month))==1:
            month="0"+str(date.month)
        else:
            month=str(date.month)
        if len(str(date.day))==1:
            day="0"+str(date.day)
        else:
            day=str(date.day)
        if len(str(date.hour))==1:
            hour="0"+str(date.hour)
        else:
            hour=str(date.hour)
        if len(str(date.minute))==1:
            minute="0"+str(date.minute)
        else:
            minute=str(date.minute)
        logs=sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B%5D=givedonate&type%5B%5D=giveitem&type%5B%5D=ao_chat&type%5B%5D=ban&type%5B%5D=kpz&type%5B%5D=jail&type%5B%5D=mute&type%5B%5D=warn&type%5B%5D=unban&type%5B%5D=unkpz&type%5B%5D=unjail&type%5B%5D=unmute&type%5B%5D=unwarn&type%5B%5D=unwarn_talon&type%5B%5D=login&type%5B%5D=disconnect&sort=desc&min_period={year}-{month}-{day}+{hour}%3A{minute}%3A00&player=QueenBot")
        logs=BeautifulSoup(logs.text,"lxml")
        stroki=logs.find_all("tr")[1:]
        if len(stroki)!=0:
            for i in stroki:
                chat_sender(" ".join(i.text.split("I:")[0].strip().split()))
        """
        return True


@app.route("/queen/chat")
def get_chat():
    return collection.find_one({"type":"chat"})["text"]


if __name__=="__main__":
    app.run(debug=False,host="0.0.0.0",port="8000")