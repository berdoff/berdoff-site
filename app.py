from pymongo import MongoClient
from flask import Flask,render_template,flash,request,redirect,session,url_for,abort
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
import requests
import certifi
import json
import re
import datetime
import time
from bs4 import BeautifulSoup
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import tok,mongo,s_key,p,token_berdoff,app_id,oauth_key,str_token,token_tg
import random
import testip
import hashlib
import aiohttp
import asyncio
import imaplib
import telebot

bot = telebot.TeleBot(token_tg)
cluster=MongoClient(mongo,tlsCAFile=certifi.where())
db=cluster["UsersData"]
collection=db["forms"]
illegals_collection=db["ILLEGALS"]
loggs=db["logs"]
rakbots=db["RAKBOT"]
rakbots_dostup=db["RAKBOT_DOSTUP"]
antiblat_collection=db["ANTIBLAT_21"]
quests_collection=db["QUESTS_21"]
slet_logs=db["SLET_LOGS_21"]

SECRET_KEY=s_key
app = Flask(__name__,static_folder="static")
app.secret_key=SECRET_KEY
login_manager = LoginManager(app)

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

def add_ghetto_zam_konf(user_id,nick_zama):
        try:
            session.method('messages.addChatUser',{'chat_id':74,'user_id':user_id})
        except:
            pass
        try:
            session.method('messages.addChatUser',{'chat_id':73,'user_id':user_id})
        except:
            pass



def add_mafii_zam_konf(user_id,nick_zama):
    try:
        session.method('messages.addChatUser',{'chat_id':76,'user_id':user_id})
    except:
        pass
    try:
        session.method('messages.addChatUser',{'chat_id':75,'user_id':user_id})
    except:
        pass


def add_kf(vk,frac_id,nick):
    frac_id=int(frac_id)
    if frac_id in [11,12,13,14,15,25]:
        add_ghetto_zam_konf(vk,nick)
    if frac_id in [16,17,18,19]:
        add_mafii_zam_konf(vk,nick)

def del_ghetto_zam_konf(user_id):
        try:
            session.method('messages.removeChatUser',{'chat_id':74,'user_id':user_id})
        except:
            b=''
        try:
            session.method('messages.removeChatUser',{'chat_id':73,'user_id':user_id})
        except:
            pass
def del_mafii_zam_konf(user_id):
    try:
        session.method('messages.removeChatUser',{'chat_id':76,'user_id':user_id})
    except:
        b=''
    try:
        session.method('messages.removeChatUser',{'chat_id':75,'user_id':user_id})
    except:
        pass

def remove_kf(id_vk): 
    del_ghetto_zam_konf(id_vk)
    del_mafii_zam_konf(id_vk)
    

def get_token(a):
    token=a.text.split("\"csrf-token\" content=\"")[1].split("\">")[0]
    return token

id_be=16


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

def chat_senderr(id,text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                print(b)
                vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'chat_id': id, 'message': text, 'disable_mentions': 1, 'random_id': 0})

def Alert(id,text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                print(b)
                vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 0, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 0, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'chat_id': id, 'message': text, 'disable_mentions': 0, 'random_id': 0})

def s_id(id,text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                print(b)
                vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'chat_id': id, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'chat_id': id, 'message': text, 'disable_mentions': 1, 'random_id': 0})


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


session=vk_api.VkApi(token=str_token)
vk=session.get_api()

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
sess = requests.session()
xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
sess.headers.update(header)
sess.cookies.update(json.loads(xsrf))




fracs={
    "11":"avatars/grove.png",
    "12":"avatars/vagos.png",
    "13":"avatars/ballas.png",
    "14":"avatars/aztec.png",
    "15":"avatars/rifa.png",
    "16":"avatars/rm.png",
    "17":"avatars/yakuza.png",
    "18":"avatars/lcn.png",
    "19":"avatars/wmc.png",
    "25":"avatars/nw.png"
}

name_fracs1={
    "11":"Grove Street",
    "12":"Los Santos Vagos",
    "13":"East Side Ballas",
    "14":"Varrios Los Aztecas",
    "15":"The Rifa",
    "16":"Russian Mafia",
    "17":"Yakuza",
    "18":"La Cosa Nostra",
    "19":"Warlock MC",
    "25":"Night Wolfs"
    
}

fracs_big={
    "11":"avatars/grove_big.png",
    "12":"avatars/vagos_big.png",
    "13":"avatars/ballas_big.png",
    "14":"avatars/aztec_big.png",
    "15":"avatars/rifa_big.png",
    "16":"avatars/rm_big.png",
    "17":"avatars/yakuza_big.png",
    "18":"avatars/lcn_big.png",
    "19":"avatars/wmc_big.png",
    "25":"avatars/nw_big.png"
}

quests_ghetto={
    "Отыграть за неделю 35 часов. [screen /myonl]":"vigs -1",
    "10 раз развести на развозчика продуктов. [screen + /time + /stats]":"vigs -1",
    "Сделать 3 рейсов на работе пилота [fraps + /time + /stats]":"vigs -1",
    "Перевести 5 грузов на работе дальнобойщика [fraps + /time + /stats]":"vigs -1",
    "Потушить 10 пожара на работе пожарного [fraps + /time + /stats]":"vigs -1",
    "Выиграть 5 каптов за сутки. [screen + /time]":"vigs -1",
    "Ограбить 3 дома [fraps + /time + /stats]":"vigs -1",
    "15 кругов вокруг стадиона на корточках. [fraps + /time + /stats]":"vigs -1",
    "Кругосветка (от Тиерры-Робады до своей респы с Сеном) [fraps + /time + /stats]":"vigs -1",
    "Убить 30 оленей в лесу. [fraps + /time + /stats]":"vigs -1",
    "Удержать военную базу ЛСа в течении 30 минут. (без суточных ограничений) [fraps + /time + /stats]":"vigs -1",
    "Закрасить 15 граффити в гетто [fraps + /time + /stats]":"vigs -1",
    "Провести капт с /members 25+. p.s. все 25 человек должны иметь 5 ранг и присутствовать на капте. [fraps + /time + /stats]":"vigs -1",
    "Посетить 2 порта за день. [screen + /time + /stats]":"vigs -1",
    "Перенести 30 мешков на работе грузчика. [screen + /time + /stats]":"vigs -1",
    "Захватить 2 Аир-Дропа. (Скриншоты с /time как лутаете сумку) [fraps + /time + /stats]":"vigs -1",
    "Перенести 15 мешков на работе грузчика. [screen + /time + /stats]":"preds -1",
    "Захватить Аир-Дроп. (Скриншоты с /time как лутаете сумку) [fraps + /time + /stats]":"preds -1",
    "Выполнить 3 задания у квестового персонажа банды. [screen + /time + /stats]":"preds -1",
    "Онлайн в /members 25+ игроков (5+ ранги) [screen + /time + /members]":"preds -1",
    " Собрать 15 закладок [fraps + /time + /stats]":"preds -1"
}

quests_mafii={
    "Выиграть 5 кораблей подряд" : "main_balls +10",
    "Выиграть 5 кораблей не подряд": "main_balls +5",
    "Захватить 4 AirDrop'a подряд":"main_balls +15",
    "Захватить 2 AirDrop'a подряд":"main_balls +5",
    "Выиграть 2 стрелы":"main_balls +5",
    "Теракт/ГРП(проведение)":"main_balls +30",
    "Ограбление банка":"main_balls +15",
    "Похищение лидера МЮ/МО/FBI/Министра":"main_balls +30",
    "Похищение лидера МЗ/СМИ/ГЦЛ/СТК/ЦБ":"main_balls +20",
    "Похищение заместителя МЮ/МО/FBI/Министра":"main_balls +15",
    "Похищение заместителя МЗ/СМИ/ГЦЛ/СТК/ЦБ": "main_balls +10",
    "Онлайн в организации больше 35 на протяжении часа (скриншоты каждые 10 минут)": "main_balls +10",
    "За отыгранную норму онлайна лидера х2":"main_balls +30",
    "За каждый десяток поднятых бизнесов":"main_balls +20"
}

vigs_cf={
    11:19,
    12:19,
    13:19,
    14:19,
    15:19,
    16:5,
    17:5,
    18:5,
    19:5,
    25:19
}


def set_warn(nick,edit,id_authora):
    prichina="Задания на сайте"
    user=illegals_collection.find_one({"nick":nick})
    user["preds"]=user["vigs"]*3+user["preds"]+int(edit)
    user["vigs"]=user["preds"]//3
    user["preds"]=user["preds"]%3
    illegals_collection.update_one({"nick":nick},{"$set":{"vigs":user["vigs"],"preds":user["preds"]}})
    illegals_collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены предупреждения @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
    chat_senderr(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены предупреждения @id{id_authora}(администратором) на {edit} по причине: {prichina}")
                
def set_vig(nick,edit,id_authora):
    print(nick,edit,id_authora)
    prichina="Задания на сайте"
    user=illegals_collection.find_one({"nick":nick})
    user["vigs"]=eval(str(user["vigs"])+edit)
    chat_senderr(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены выговоры @id{id_authora}(администратором) на {edit} по причине: {prichina} ")
    illegals_collection.update_one({"nick":nick},{"$set":{"vigs":user["vigs"]}})
    illegals_collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены выговоры @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})

class User():

    def fromDB(self,uid):
        if illegals_collection.count_documents({"id_vk":uid})!=0:
            self.__user=illegals_collection.find_one({"id_vk":uid})
        else:
            self.__user={"id_vk":uid,"dostup":"-1"}
        return self

    

    def create(self,user):
        self.__user=user
        return self

    def get_id(self):
        return str(self.__user["id_vk"])

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def nick(self):
        return self.__user["nick"]

    def dostup(self):
        return self.__user["dostup"]
    
    def dostup_int(self):
        return int(self.__user["dostup"])

    def rank(self):
        return self.__user["rank"]
    
    def ava_min(self):
        return fracs[str(self.__user["frac_id"])]
    
    def ava_big(self):
        return fracs_big[str(self.__user["frac_id"])]

    def frac(self):
        return name_fracs1[self.__user["frac_id"]]
    
    def balls(self):
        return self.__user["main_balls"]
    
    
    def frac_id(self):
        return self.__user["frac_id"]

    def vk(self):
        return "https://vk.com/id"+self.__user["id_vk"]
    
    def add_data(self):
        return self.__user["add_data"]
    
    def srok_data(self):
        return self.__user["srok_data"]
    
    def vigs(self):
        return self.__user["vigs"]
    
    def preds(self):
        return self.__user["preds"]
    
    def type_add(self):
        return self.__user["type_add"]
    

@login_manager.user_loader
def load_user(user_id):
    return User().fromDB(user_id)

trusted_ips = ['45.93.200.98', '185.36.143.118', '188.225.43.225','46.0.19.168',"162.158.87.148"]




@app.route("/")
def main():
    return render_template("index.html")

@app.route("/profile")
@login_required
def profile():
    if request.method=="GET" or request.method=="POST":
        if current_user.dostup()!="-1":
            if request.args.get("id") is not None: 
                return render_template("stats.html",c_user=current_user,user=illegals_collection.find_one({"id_vk":request.args.get("id")}), ava=fracs_big[str(illegals_collection.find_one({"id_vk":request.args.get("id")})["frac_id"])],dostup_int=int(illegals_collection.find_one({"id_vk":request.args.get("id")})["dostup"]),name_frac=name_fracs1)
            else:
                return "Не указан id профиля"
            
            
        else:
            return render_template("access_denied.html")


@app.route("/members")
@login_required
def members():
    if request.method=="GET" or request.method=="POST":
        if current_user.dostup()!="-1":
            return render_template("members.html",user=current_user,leaders=illegals_collection.find({"dostup":"1"}).sort("frac_id"),fracs_big=fracs_big)
            
        else:
            return render_template("access_denied.html")


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/auth')


@app.route("/antiblat")
@login_required
def antiblat():
    if request.method=="GET" or request.method=="POST":
        print(current_user.dostup())
        if current_user.dostup()!="-1":
            if int(current_user.dostup())==1:
                if request.args.get("zam_nick") is not None and request.args.get("zam_vk") is not None and request.args.get("zam_add") is not None and current_user.dostup()=="1" and (antiblat_collection.count_documents({"zam_nick":request.args.get("zam_nick"),"status":0})==0):
                    zam_nick=request.args.get("zam_nick")
                    if current_user.frac_id() in [11,12,13,14,15,25]:
                        if (request.args.get("zam_stats") is not None) :
                            id_vk=(vk_session.method('utils.resolveScreenName',{"screen_name":request.args.get("zam_vk").split("/")[-1]}))
                            if id_vk["type"]=="user":
                                id_vk=str(id_vk["object_id"])
                                
                                antiblat_collection.insert_one({"nick":current_user.nick(),"zam_nick":request.args.get("zam_nick"),"zam_add":request.args.get("zam_add"),"frac_id":current_user.frac_id(),"frac":name_fracs1[str(current_user.frac_id())],"id_vk":id_vk,"status":0,"ava":fracs[str(current_user.frac_id())],"stats":request.args.get("zam_stats")})
                                return "<script>alert('Заявка добавлена');</script>"
                    else:
                        if (request.args.get("zam_bio") is not None) and (request.args.get("zam_docs") is not None) and (request.args.get("zam_stats") is not None):
                            id_vk=(vk_session.method('utils.resolveScreenName',{"screen_name":request.args.get("zam_vk").split("/")[-1]}))
                            if id_vk["type"]=="user":
                                id_vk=str(id_vk["object_id"])
                                
                                antiblat_collection.insert_one({"nick":current_user.nick(),"zam_nick":request.args.get("zam_nick"),"zam_add":request.args.get("zam_add"),"frac_id":current_user.frac_id(),"frac":name_fracs1[str(current_user.frac_id())],"id_vk":id_vk,"status":0,"bio":request.args.get("zam_bio"),"docs":request.args.get("zam_docs"),"ava":fracs[str(current_user.frac_id())],"stats":request.args.get("zam_stats")})
                                return "<script>alert('Заявка добавлена');</script>"
            else:
                if request.args.get("add") is not None and request.args.get("zam_nick") is not None:
                    add=request.args.get("add")
                    zam_nick=request.args.get("zam_nick").strip()
                    zam=antiblat_collection.find_one({"status":0,"zam_nick":zam_nick})
                    id_authora=current_user.get_id()
                    if add=="1":
                        print(zam["zam_add"])
                        if zam["zam_add"]=="Поставил":
                            today_date=datetime.datetime.today()
                            date_today=str(today_date.day)+'.'+str(today_date.month)+'.'+str(today_date.year)
                            srok_data=today_date+datetime.timedelta(days=30)
                            srok_data=str(srok_data.day)+'.'+str(srok_data.month)+'.'+str(srok_data.year)
                            zam["add_data"]=date_today
                            zam["srok_daya"]=srok_data
                            zam["dostup"]="0"
                            zam["main_balls"]=0
                            zam["vigs"]=0
                            zam["preds"]=0
                            zam["nick"]=zam["zam_nick"]
                            zam["rank"]="Заместитель"
                            zam["type_add"]="АБ"
                            add_kf(zam["id_vk"],zam["frac_id"],zam["nick"])
                            illegals_collection.insert_one(zam)
                            
                        elif zam["zam_add"]=="снял":
                            try:
                                remove_kf(zam["id_vk"])
                                illegals_collection.delete_one({"id_vk":zam["id_vk"]})
                                
                            except:
                                pass
                        else:
                            pass
                    elif add=="0":
                        chat_senderr(vigs_cf[zam["frac_id"]],f"Антиблат на игрока {zam_nick} отказан @id{id_authora}(администратором)!")
                        

                    else:
                        return("Ошибка")
                    antiblat_collection.update_one({"status":0,"zam_nick":zam_nick},{"$set":{"status":1}})
                    return redirect("/antiblat")
                else:
                    pass
            return render_template("antiblat.html",user=current_user,users=antiblat_collection.find({"status":0}))
            
        else:
            return render_template("access_denied.html")

@app.route("/quests")
@login_required
def quests():
    if request.method=="GET" or request.method=="POST":
        if current_user.dostup()!="-1":
            if current_user.dostup_int()<=1:
                if request.args.get("quest") is not None and request.args.get("docs") is not None:
                    if request.args.get("quest") in quests_ghetto:
                        nagrada=quests_ghetto[request.args.get("quest")]
                        quests_collection.insert_one({"frac_id":current_user.frac_id(),"nick":current_user.nick(),"ava":fracs[str(current_user.frac_id())],"quest":request.args.get("quest"),"docs":request.args.get("docs"),"status":0,"nagrada":nagrada,"id":quests_collection.count_documents({})+1})
                        return "Задание отправлено на проверку"
                    elif request.args.get("quest") in quests_mafii:
                        nagrada=quests_mafii[request.args.get("quest")]
                        quests_collection.insert_one({"frac_id":current_user.frac_id(),"nick":current_user.nick(),"ava":fracs[str(current_user.frac_id())],"quest":request.args.get("quest"),"docs":request.args.get("docs"),"status":0,"nagrada":nagrada,"id":quests_collection.count_documents({})+1})
                        return "Задание отправлено на проверку"
                    else:
                        return "Несуществующее задание"
            else:
                if request.args.get("acc") is not None and request.args.get("id") is not None:
                    frac_id=quests_collection.find_one({"id":int(request.args.get("id"))})["frac_id"]
                    quest=quests_collection.find_one({"id":int(request.args.get("id"))})["quest"]
                    nick=illegals_collection.find_one({"frac_id":frac_id,"dostup":"1"})["nick"]
                    nagrada=quests_collection.find_one({"id":int(request.args.get("id"))})["nagrada"]
                    user=illegals_collection.find_one({"nick":nick})
                    id_authora=current_user.get_id()
                    if request.args.get("acc")=="1":
                        
                        edit=nagrada.split()[1]
                        quests_collection.update_one({"id":int(request.args.get("id"))},{"$set":{"status":1}})
                        if nagrada.split()[0]=="main_balls":
                            prichina="Задания на сайте"
                            edit=edit.replace(",",".")
                            user["main_balls"]=eval(str(user["main_balls"])+edit)
                            illegals_collection.update_one({"nick":nick},{"$set":{"main_balls":user["main_balls"]}})
                            illegals_collection.update_one({"nick":nick},{"$set":{"main_balls_history":user["main_balls_history"]+f"\nИзменены баллы @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
                            chat_senderr(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены основные баллы @id{id_authora}(администратором) на {edit} по причине: {prichina}")
                        elif nagrada.split()[0]=="vigs":
                            set_vig(nick,edit,id_authora)
                        elif nagrada.split()[0]=="preds":
                            set_warn(nick,edit,id_authora)
                        else:
                            return "Ошибка"
                    else:
                        quests_collection.update_one({"id":int(request.args.get("id"))},{"$set":{"status":1}})
                        chat_senderr(vigs_cf[user["frac_id"]],f"Лидеру {nick} отказано задание {quest} @id{id_authora}(администратором)")
                        return redirect("/quests")
                        
            return render_template("quests.html",user=current_user,quests_mafii=quests_mafii,quests_ghetto=quests_ghetto,name_fracs=name_fracs1,questss=quests_collection.find({"status":0}),avas=fracs)
            
        else:
            return render_template("access_denied.html")


@app.route("/api/authlogs",methods=["GET","POST"])
def delll():
    if request.remote_addr not in trusted_ips:
        abort(404)
    else:
        global logs
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
        if request.method=="GET" or request.method=="POST":
            code=request.form.get("code")
            sess = requests.session()
            a=sess.get("https://arizonarp.logsparser.info/login")
            token=get_token(a)
            print(token)
            a=sess.post("https://arizonarp.logsparser.info/login",data={"name":"Lorenzo_Almas","password":p,"_token":token})
            token=get_token(a)
            print(token)
            
            a=sess.post("https://arizonarp.logsparser.info/authenticator",data={"_token":token,"code":code},headers=header)
            if "Queen-Creek" in a.text:
                loggs.update_one({"type":"token"},{"$set":{"session":str({"XSRF-TOKEN":a.cookies["XSRF-TOKEN"],"arizonarp_session":a.cookies["arizonarp_session"]})}})
                return "Вошло\n\n"+str(a.cookies)
            else:
                return "Не вошло"+" "+get_token(a)+" "+code+"\n"

@app.route("/api/newcapture",methods=["GET","POST"])
def new_capture():
    if request.method=="GET" or request.method=="POST":
        if request.remote_addr not in trusted_ips:
            abort(404)
        else:
            text=request.form.get("text")
            s_id(6,str(text).replace("{B7AFAF}","")[2:-2])
            return True


@app.route("/checklogs",methods=["GET","POST"])
def dwadwadwa():
    global logs
    if request.method=="GET" or request.method=="POST":
        if request.remote_addr not in trusted_ips:
            abort(404)
        else:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
            sess.headers.update(header)
            sess.cookies.update(json.loads(xsrf))
            a=sess.get("https://arizonarp.logsparser.info/")
            if "Queen-Creek" in a.text:
                return BeautifulSoup(a.text,"lxml").find("a",class_="nav-link dropdown-toggle").text
            else:
                return a.text
                #return "-\n\n"+xsrf



@app.route("/api/slet_log",methods=["GET","POST"])
def slet_log():
    if request.method=="GET" or request.method=="POST":
        token=request.form.get("token")
        if token==token_berdoff:
            nick=request.form.get("nick")
            ids=request.form.get("ids")
            typee=request.form.get("type")
            tm=request.form.get("tm")
            code=request.form.get("code")
            slet_logs.insert_one({"nick":nick,"id":ids,"type":typee,"tm":tm,"ctime":int(str(time.time()).split(".")[0]),"dtime":int(str(time.time()).split(".")[0])+10800,"code":code})
            return True


@app.route("/api/topsecret",methods=["GET","POST"])
def topsecret():
    if request.method=="GET" or request.method=="POST":
        token=request.form.get("token")
        if token==token_berdoff:
            nick=request.form.get("nick")
            id_ka=request.form.get("id")
            Alert(1,f"@berdofff @lorenzo_almas\n Красный на сервере: {nick}[{id_ka}]")
            Alert(1,f"@berdofff @lorenzo_almas\n Красный на сервере: {nick}[{id_ka}]")
            Alert(1,f"@berdofff @lorenzo_almas\n Красный на сервере: {nick}[{id_ka}]")
            bot.send_message("-834352877", f"@berdofff @maryan_solonynko\n Красный на сервере: {nick}[{id_ka}]")
            bot.send_message("-834352877", f"@berdofff @maryan_solonynko\n Красный на сервере: {nick}[{id_ka}]")
            bot.send_message("-834352877", f"@berdofff @maryan_solonynko\n Красный на сервере: {nick}[{id_ka}]")

@app.route("/api/accepts",methods=["GET","POST"])
def accepts():
    if request.method=="GET" or request.method=="POST":
        token=request.form.get("token")
        if token==token_berdoff:
            nick=request.form.get("nick")
            chat_senderr(1,f"!ацепт {nick}")
        
@app.route("/auth",methods=["GET","POST"])
def auth_vk():
    if request.method=="GET" or request.method=="POST":
        
        uid=request.args.get("uid")
        hash=request.args.get("hash")
        if uid is not None and hash is not None:
            code=app_id+uid+oauth_key
            print(code)
            code=hashlib.md5(code.encode("utf-8")).hexdigest()

            if code==hash:
                if illegals_collection.count_documents({"id_vk":uid})!=0:
                    user=illegals_collection.find_one({"id_vk":uid})
                else:
                    user={"id_vk":uid,"dostup":"-1"}
                userlogin=User().create(user)
                login_user(userlogin,remember=True)
                return redirect("/profile?id="+current_user.get_id())
        else:
            return render_template("index1.html")
            


@app.route("/loadlogsdawdawdwadwadwadwadwa2121",methods=["GET","POST"])
def load_7days():
    global logs
    if request.method=="GET" or request.method=="POST":
        nick=request.form.get("nick")
        token=request.form.get("token")
        server=request.form.get("server")
        print("1")
        if len(token)<40 and token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
            sess.headers.update(header)
            sess.cookies.update(json.loads(xsrf))
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
                year_min = str(date.year)
                if len(str(date.month)) == 1:
                    month_min = "0" + str(date.month)
                else:
                    month_min = str(date.month)
                if len(str(date.day)) == 1:
                    day_min = "0" + str(date.day)
                else:
                    day_min = str(date.day)
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
                print("Load logs")
                url=""
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year_min}-{month_min}-{day_min}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                while "Игрок" in logs.text or "Администратор" in logs.text:
                    print(k)
                    logs=BeautifulSoup(logs.text,"lxml")
                    stroka=logs.find_all("tr")[1:]
                    for i in stroka:
                        if "авторизовался" in i.text or "авторизация: Есть" in i.text:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split())+" [R-IP: "+i.find_all("span", class_="badge badge-primary")[0].text+" L-IP: "+i.find_all("span", class_="badge badge-secondary")[0].text+"]")
                        elif "$" in i.text:
                            vc_money=i.find_all("div",class_="app__hidden")[0].find_all("li")[1].find("code").text
                            money_nal=i.find_all("code")[1].text
                            money_bank=i.find_all("code")[2].text
                            donate=i.find_all("code")[3].text
                            if server=="201":
                                strr.append(" ".join(i.text.split("I:")[0].strip().split())+f""" (<font color="#00FF00">VC: {vc_money}$</font>,<font color="#006400">Bank: {money_bank}$</font>,<font color="#B22222">Donate: {donate}</font>)""")
                            else:
                                strr.append(" ".join(i.text.split("I:")[0].strip().split())+f""" (<font color="#00FF00">Money: {money_nal}$</font>,<font color="#006400">Bank: {money_bank}$</font>,<font color="#B22222">Donate: {donate}</font>)""")
                        else:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split()))
                    k+=1
                    logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year_min}-{month_min}-{day_min}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                  
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


@app.route("/loadlogsdawdawdwadwadwadwadwa212132222",methods=["GET","POST"])
def load_30days():
    global logs
    if request.method=="GET" or request.method=="POST":
        nick=request.form.get("nick")
        token=request.form.get("token")
        server=request.form.get("server")
        print("1")
        if len(token)<40 and token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
            sess.headers.update(header)
            sess.cookies.update(json.loads(xsrf))
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
                date = date - datetime.timedelta(days=30)
                year_min = str(date.year)
                if len(str(date.month)) == 1:
                    month_min = "0" + str(date.month)
                else:
                    month_min = str(date.month)
                if len(str(date.day)) == 1:
                    day_min = "0" + str(date.day)
                else:
                    day_min = str(date.day)
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
                print("Load logs")
                url=""
                logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year_min}-{month_min}-{day_min}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                while "Игрок" in logs.text or "Администратор" in logs.text:
                    print(k)
                    logs=BeautifulSoup(logs.text,"lxml")
                    stroka=logs.find_all("tr")[1:]
                    for i in stroka:
                        if "авторизовался" in i.text or "авторизация: Есть" in i.text:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split())+" [R-IP: "+i.find_all("span", class_="badge badge-primary")[0].text+" L-IP: "+i.find_all("span", class_="badge badge-secondary")[0].text+"]")
                        elif "$" in i.text:
                            vc_money=i.find_all("div",class_="app__hidden")[0].find_all("li")[1].find("code").text
                            money_nal=i.find_all("code")[1].text
                            money_bank=i.find_all("code")[2].text
                            donate=i.find_all("code")[3].text
                            if server=="201":
                                strr.append(" ".join(i.text.split("I:")[0].strip().split())+f""" (<font color="#00FF00">VC: {vc_money}$</font>,<font color="#006400">Bank: {money_bank}$</font>,<font color="#B22222">Donate: {donate}</font>)""")
                            else:
                                strr.append(" ".join(i.text.split("I:")[0].strip().split())+f""" (<font color="#00FF00">Money: {money_nal}$</font>,<font color="#006400">Bank: {money_bank}$</font>,<font color="#B22222">Donate: {donate}</font>)""")
                        else:
                            strr.append(" ".join(i.text.split("I:")[0].strip().split()))
                    k+=1
                    logs=sess.get(f"https://arizonarp.logsparser.info/?server_number={server}&sort=desc&min_period={year_min}-{month_min}-{day_min}+00%3A00%3A00&max_period={year_today}-{month_today}-{day_today}+00%3A00%3A00&player={id_acc}&limit=1000&page={k}")
                  
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
    if (request.method=="GET" or request.method=="POST"):
        token=request.args.get('token')
        print(len(token))
        if len(token)==18:
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
    
    if (request.method=="GET" or request.method=="POST"):
        token = request.form.get("token")
        nick = request.form.get("nick")
        server=request.form.get("server")
        print(request.remote_addr)
        print(nick,token)
        reps=False
        if token == token_berdoff:
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
            sess.headers.update(header)
            sess.cookies.update(json.loads(xsrf))
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
                print(server)
                try:
                    lvl_adm=stroki[0].find_all("div",class_="app__hidden")[0].find_all("li")[6].find("code").text.strip()
                except:
                    lvl_adm="0"
                print(lvl_adm)
                if str(lvl_adm)!="0":
                    reps=True
                print(reps)
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
                if reps:
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
                online["reports"]["check"]=str(reps)
                return online

            else:
                return {"status": "ne ok", "reason": "Логи не авторизованы"}


@app.route("/api/getpunish",methods=["GET","POST"])
def get_punish():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        token=request.form.get("token")
        nick=request.form.get("nick")
        if token==token_berdoff:
            return sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B%5D=rmute&type%5B%5D=unrmute&type%5B%5D=skick&type%5B%5D=weap&type%5B%5D=spawnplayer&type%5B%5D=ban&type%5B%5D=jail&type%5B%5D=kick&type%5B%5D=mute&type%5B%5D=uval&type%5B%5D=warn&type%5B%5D=banip&type%5B%5D=unban&type%5B%5D=unjail&type%5B%5D=unmute&type%5B%5D=unwarn&type%5B%5D=unwarn_talon&sort=desc&player={nick}").text



@app.route("/api/getrakbot",methods=["GET","POST"])
def get_rakbot():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        rks=[]
        for i in rakbots.find():
            rks.append({"vk":i["vk"],"nick":i["nick"],"IP":i["IP"]})
            ttime=i["time"]
            if int(time.time())-int(ttime)>300:
                rakbots.delete_one({"vk":i["vk"],"time":ttime})
                send_to_user(i["vk"],f"Снятие ракбота завершено по истечению 5 минут")
        return rks
"""
@app.route("/api/sendbiz",methods=["GET","POST"])
def send_biz():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        frac=request.args.get("frac")
        bizlist=request.form.get("bizlist")
        #bizlist=json.loads(bizlist)
        loggs.update_one({"type":"biz"},{"$set":{str(frac):str((bizlist))}})
"""
@app.route("/api/get_admins",methods=["GET","POST"])
def get_admins():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        token=request.args.get("token")
        vk=request.args.get("vk")
        if token==token_berdoff:
            admin=requests.get("http://admin-tools.ru/vkbot/api_admins.php?type=1&token=sdf4632f4sd132g454hytjtyuire1d1s3a4864sdf65rte7yuirt34ewfdsf41fdg56jsdf&server=21").text
            return admin
        else:
            return "Access Denied"
        loggs.update_one({"type":"biz"},{"$set":{str(frac):str((bizlist))}})

@app.route("/api/addrakbot",methods=["GET","POST"])
def add_rakbot():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        nick=request.form.get("nick")
        ip=request.form.get("ip")
        tttime=int(str(time.time()).split(".")[0])
        vk=request.form.get("vk")
        token=request.form.get("token")
        if token==token_berdoff:
            if rakbots.count_documents({"nick":nick})==0:
                rakbots.insert_one({"nick":nick,"vk":vk,"IP":ip,"time":tttime})
            else:
                rakbots.delete_many({"nick":nick})
                rakbots.insert_one({"nick":nick,"vk":vk,"IP":ip,"time":tttime})

@app.route("/api/dellrakbot",methods=["GET","POST"])
def dell_rakbot():
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
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
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        token=request.form.get("token")
        pages=1
        if token==token_berdoff:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            sess = requests.session()
            xsrf=loggs.find_one({"type":"token"})["session"].replace("\'","\"")
            sess.headers.update(header)
            sess.cookies.update(json.loads(xsrf))
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
    if (request.method=="GET" or request.method=="POST") and request.remote_addr in trusted_ips:
        token=request.args.get("token")
        check=request.args.get("check")
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
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
    app.run(debug=True,host="0.0.0.0",port="8000")