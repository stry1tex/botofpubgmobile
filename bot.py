import telebot
import requests
import time
import json
import sqlite3
from telebot import types
from random import randint
from config import bot, idadmin, qiwinumber, privet, kupit, otzyvy, probota, \
 texpoderjka,btnkupit, btnotzyvy, btnprobota, btntexpoderjka,btnotmena, \
 otvet_otmena,nepravilni_id,btnceny,otvet_ceny,skolkouc,minuc,maxuc,errorminuc,errormaxuc, \
 cena, oshibkasumm,token_qiwi,neoplatil,oplatil,btnref,bot_name,bonusuc





@bot.message_handler(commands=['start'])
def send_welcome(message):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(f"select count(*) from users where id = {message.chat.id}")
    if cur.fetchone()[0] == 0:
        con.commit()
        if message.chat.id == idadmin:
            bot.send_message(message.chat.id, privet, reply_markup=adminbtns())
        else:
            bot.send_message(message.chat.id, privet, reply_markup=userbtns())

        ref = message.text
        if len(ref) != 6:
            try:
                ref = int(ref[7:])
                con = sqlite3.connect("data.db")
                cur = con.cursor()
                cur.execute(f"select count(*) from users where id = {ref}")
                if cur.fetchone()[0] != 0:
                    con.commit()
                    boss = ref
                else:
                    con.commit()
                    boss = idadmin
            except:
                boss = idadmin
        else:
            boss = idadmin

        id = message.chat.id
        name = (f"{message.chat.first_name} {'|'} {message.chat.last_name}")
        referals = 0
        user_name = message.chat.username
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO users (id,name,referals,boss, username) "
                    f"VALUES ({id},\"{name}\",{referals},{boss}, \"{user_name}\")")
        con.commit()

        
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute(f"SELECT referals FROM users WHERE id = {boss}")
        referal = cur.fetchone()[0]
        referals = referal + 1
        con.commit()
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET referals = {referals} WHERE id = {boss}")
        con.commit()


    else:
        con.commit()
        if message.chat.id == idadmin:
            bot.send_message(message.chat.id, privet, reply_markup=adminbtns())
        else:
            bot.send_message(message.chat.id, privet, reply_markup=userbtns())


     


@bot.message_handler(content_types="text")
def get_text_message(message):
    if message.text == "Рассылка" and message.chat.id == idadmin:
        bot.send_message(message.from_user.id, "Введите текст рассылки\n\nЕсли хотите отменить рассылку напишите '-'")
        bot.register_next_step_handler(message, admin_rassilka)

    elif message.text == "Статистика" and message.chat.id == idadmin:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT COUNT (*) FROM users")
        number = cur.fetchone()[0]
        bot.send_message(message.from_user.id, f"Всего пользователей в боте - {number}")

    elif message.text == btnkupit:
        bot.send_message(message.from_user.id,kupit,reply_markup=otmena())
        bot.register_next_step_handler(message, account)

    elif message.text == btnotzyvy:
        bot.send_message(message.from_user.id,otzyvy)

    elif message.text == btnprobota:
        bot.send_message(message.from_user.id,probota)

    elif message.text == btntexpoderjka:
        bot.send_message(message.from_user.id,texpoderjka)
    elif message.text == btnceny:
        bot.send_message(message.from_user.id,otvet_ceny)
    elif message.text == btnref:
    	con = sqlite3.connect("data.db")
    	cur = con.cursor()
    	cur.execute(f"SELECT referals FROM users WHERE id = {message.chat.id}")
    	referals = cur.fetchone()[0]
    	bonusplus=referals*bonusuc
    	reflnk=f"http://t.me/{bot_name}?start={message.chat.id}"
    	otvet_ref = f"👥 У нас действует реф. система\n\nЗа каждого приглашенного друга вы получите {bonusuc}uc\n\nВаша реф. ссылка - {reflnk}\nВы пригласили {referals} 👨‍👨‍👦‍👦\nВаш бонус к пополнению {bonusplus}uc(Вы получите свои бонусные uc вместе с заказом)\n\nПриглашайте друзьей и выгодно пополнайте uc вместе !"
    	bot.send_message(message.from_user.id,otvet_ref)


    elif message.text == btnotmena:
        if message.chat.id == idadmin:
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=adminbtns())
            bot.register_next_step_handler(message, get_text_message)

        else:
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=userbtns())
            bot.register_next_step_handler(message, get_text_message)

@bot.message_handler(content_types="text")
def account(message):
    if message.text.isdigit():
        if int(message.text)>=10000 and int(message.text)< 999999999999:
            bot.send_message(message.from_user.id,skolkouc)
            bot.register_next_step_handler(message, skokuc)
        else:
            bot.send_message(message.from_user.id,nepravilni_id)
            bot.register_next_step_handler(message, account)

    elif message.text == btnotmena:
        if message.chat.id == idadmin:
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=adminbtns())
            bot.register_next_step_handler(message, get_text_message)

        else:
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=userbtns())
            bot.register_next_step_handler(message, get_text_message)
    else:   
        bot.send_message(message.from_user.id,nepravilni_id)
        bot.register_next_step_handler(message, account)


@bot.message_handler(content_types="text")
def skokuc(message):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if message.text.isdigit():
        summ = int(message.text)
        if summ < minuc:
            bot.send_message(message.from_user.id,errorminuc)
            bot.register_next_step_handler(message, skokuc)
        elif summ > maxuc:
            bot.send_message(message.from_user.id,errormaxuc)
            bot.register_next_step_handler(message, skokuc)
        else:
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            itog = (summ * cena)/1000
            comment = randint(10000, 9999999)
            cur.execute(f"INSERT INTO oplata (id, code) VALUES({message.chat.id}, {comment})")
            con.commit()
            markup_inline = types.InlineKeyboardMarkup()
            proverka = types.InlineKeyboardButton(text='Проверить оплату' ,callback_data='prov')
            markup_inline.add(proverka)
            bot.send_message(message.from_user.id,f'♻️Переведите {itog}₽ на счет Qiwi\n\nНомер: `{qiwinumber}`\nКомментарий `{comment}` \n \nБыстрая форма оплаты: [ОПЛАТА](https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={qiwinumber}&amountInteger={itog}&amountFraction=0&currency=643&extra%5B%27comment%27%5D={comment})\n\n_Нажмите на номер и комментарий, чтобы их скопировать_',
                             parse_mode='Markdown',reply_markup=markup_inline)

            bot.register_next_step_handler(message, zakaz)


    elif message.text == btnotmena:
        if message.chat.id == idadmin:
            
            cur.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
            con.commit()
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=adminbtns())
            bot.register_next_step_handler(message, get_text_message)

        else:
            
            cur.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
            con.commit()
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=userbtns())
            bot.register_next_step_handler(message, get_text_message)   

        
         

    else:
        bot.send_message(message.from_user.id,oshibkasumm)
        bot.register_next_step_handler(message, skokuc)


@bot.message_handler(content_types="text")
def zakaz(message):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if message.text == btnotmena:
        if message.chat.id == idadmin:
            
            cur.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
            con.commit()
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=adminbtns())
            bot.register_next_step_handler(message, get_text_message)

        else:
            
            cur.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
            con.commit()
            bot.send_message(message.from_user.id,otvet_otmena,reply_markup=userbtns())
            bot.register_next_step_handler(message, get_text_message)

    elif message.text == "proverkanasliv":
        bot.send_message(message.from_user.id,"bot ot baci")
        bot.register_next_step_handler(message, zakaz)

    else:
        bot.send_message(message.from_user.id,"Завершите заказ либо нажмите отмена.")
        bot.register_next_step_handler(message, zakaz)




@bot.message_handler(content_types="text")
def admin_rassilka(message):
	if message.text == "-":
		bot.send_message(message.from_user.id, "Рассылка отменена")
		bot.register_next_step_handler(message, get_text_message)
	else:

	    con = sqlite3.connect("data.db")
	    cur = con.cursor()
	    bot.send_message(message.from_user.id, "Рассылка успешно начата")
	    cur.execute("SELECT id FROM users")
	    id = cur.fetchall()
	    for i in id:
	        try:
	            bot.send_message(i[0], f"{message.text}")
	            time.sleep(0.1)
	        except:
	            pass
	    bot.send_message(message.from_user.id, "Рассылка успешно завершена")



@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if call.data == 'prov':
        
        user_id = call.message.chat.id
        QIWI_TOKEN = token_qiwi
        QIWI_ACCOUNT = str(qiwinumber)
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
        parameters = {'rows': '50'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments',params=parameters)
        req = json.loads(h.text)
        try:
            
            cur.execute(f"SELECT * FROM oplata WHERE id = {user_id}")
            result = cur.fetchone()
            comment = str(result[1])
            
            for x in range(len(req['data'])):
                if req['data'][x]['comment'] == comment:
                    itog = (req['data'][x]['sum']['amount'])
                    cur.execute(f"DELETE FROM oplata WHERE id = {user_id}")
                    con.commit()

                    bot.send_message(idadmin,f"💸 Мамонтизация прошла успешно 💸\n\n   Пополнение {itog}р")
                    bot.send_message(call.message.chat.id,oplatil)
                    break
                else:
                    
                    bot.send_message(call.message.chat.id,neoplatil)
                    bot.register_next_step_handler(message, skokuc)
                    break


        except:
            pass

    else:
        pass


def userbtns():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(btnkupit)
    key2 = types.KeyboardButton(btnotzyvy)
    key3 = types.KeyboardButton(btnprobota)
    key4 = types.KeyboardButton(btntexpoderjka)
    key8 = types.KeyboardButton(btnceny)
    key9 = types.KeyboardButton(btnref)


    markup.add(key1)
    markup.add(key8,key9)
    markup.add(key3, key4)
    markup.add(key2)

    return markup


def adminbtns():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(btnkupit)
    key2 = types.KeyboardButton(btnotzyvy)
    key3 = types.KeyboardButton(btnprobota)
    key4 = types.KeyboardButton(btntexpoderjka)
    key8 = types.KeyboardButton(btnceny)
    key9 = types.KeyboardButton(btnref)
    key6 = types.KeyboardButton("Рассылка")
    key5 = types.KeyboardButton("Статистика")

    markup.add(key1)
    markup.add(key8,key9)
    markup.add(key3, key4)
    markup.add(key2)
    markup.add(key5, key6)

    return markup

def otmena():
    markup = types.ReplyKeyboardMarkup(True)
    key8 = types.KeyboardButton(btnotmena)

    markup.add(key8)

    return markup



if __name__ == '__main__':
    bot.polling(none_stop=True)





