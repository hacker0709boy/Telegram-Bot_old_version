import telebot
from telebot import types
import mysql.connector
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

bot = telebot.TeleBot("5135469781:AAFM7cBRz2Ko8TZp5ublRXQ4WgbG_erEnV0")
db = mysql.connector.connect(
            host="hasabym.com",
            user="u1184328_telegrm",
            passwd="telegram_db1",
            port="3306",
            database="u1184328_telegrm")
user_data = []

@bot.message_handler(commands=['start'])
def fn_check_inv_tlgrm_id(message):
    try:  
        bot.send_message(message.chat.id, "Welcome to TudanaBot")
        user_id = message.from_user.id
        
        command = message.text
        
        db = mysql.connector.connect(
            host="hasabym.com",
            user="u1184328_telegrm",
            passwd="telegram_db1",
            port="3306",
            database="u1184328_telegrm")
############################     FINDING USER ON DATABASES      ######################################
        if len(str(user_id)) > 0 :
          cursor = db.cursor()
          cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result, ifnull(type_id, 0) as type_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id)  + "'")
          result = cursor.fetchone()
############################      USER NOT FOUND ON DATABASES    ####################################
          if result[0] != 'EXISTS' and result[1] == 0:
            bot.reply_to(message, "Ulanyjy ID tapylmady!")
            user_not_found = bot.send_message(message.chat.id, "Sahsy acar kodynyzy girin:")
            bot.register_next_step_handler(user_not_found, password_step)
############################      USER EXIST ON DATABASES / WELCOME PROCCESS      #######################################
          else:
            cursor = db.cursor()
            cursor.execute("SELECT investor_id FROM tbl_investors WHERE investor_telegram_id = '" + str(user_id) + "'")
            id_f = cursor.fetchone()
            tel_inv_id = id_f[0]
            print(tel_inv_id)
            
            user_data.append(tel_inv_id)
            print("user data",user_data)
            bot.reply_to(message, "Hosgeldiniz!!")
            investor_markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Balance", callback_data="ba")
            item2 = types.InlineKeyboardButton("Image", callback_data="img")
            investor_markup.add(item2, item1)
            
            if result[1] == 2:
              inv_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name}, {0.last_name}".format(message.from_user, message.from_user), reply_markup = investor_markup)
              

            else:
              admin_markup = types.InlineKeyboardMarkup(row_width=2)
              button1 = types.InlineKeyboardButton("Balance", callback_data="ba")
              button2 = types.InlineKeyboardButton("Image", callback_data="img")
              button3 = types.InlineKeyboardButton("Upload Photo", callback_data="uph")
              button4 = types.InlineKeyboardButton("Delete Photo", callback_data="dph")

              admin_markup.add(button1, button2,button3,button4)
              print("admin")
              admin_welcome_message = bot.send_message(message.chat.id, "Salam {0.first_name}, {0.last_name}".format(message.from_user, message.from_user), reply_markup = admin_markup)

        else:
           bot.reply_to(message, "Ulanyjy ID bosh alyndy!")
        
    except SyntaxError:
        bot.reply_to(message, "Start etmekde yalnyshlyk!")







def find_certificate_code(message):
  try:  
      user_id = message.from_user.id
      cert_code = message.text
      cursor = db.cursor()
      cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN 'EXISTS' ELSE 'NOT_EXISTS' END AS result FROM tbl_investment WHERE certificate_code = '" + str(cert_code) + "' AND investor_id = '" + str(user_data[0]) + "'")
      q = cursor.fetchone()
      print(q)
      if q[0] != 'EXISTS':
        bot.reply_to(message, "CERTIFICATE CODE NOT FOUNF 404!")
      else:
        cursor.execute("UPDATE tbl_investors SET investor_telegram_id = '" + str(user_id) + "' WHERE investor_id = '" + str(user_data[0]) + "'")
        db.commit()
        bot.reply_to(message, "Hosgeldiniz!!")
        if user_data[1] == '1':
          investor_markup = types.InlineKeyboardMarkup(row_width=2)
          item1 = types.InlineKeyboardButton("Balance", callback_data="ba")
          item2 = types.InlineKeyboardButton("Image", callback_data="img")
          investor_markup.add(item2, item1)
          bot.reply_to(message, "Hosgeldiniz!!", reply_markup=investor_markup)

        if user_data[1] == '2':
          admin_markup = types.InlineKeyboardMarkup(row_width=2)
          button1 = types.InlineKeyboardButton("Balance", callback_data="ba")
          button2 = types.InlineKeyboardButton("Image", callback_data="img")
          button3 = types.InlineKeyboardButton("Upload Photo", callback_data="uph")
          button4 = types.InlineKeyboardButton("Delete Photo", callback_data="dph")

          admin_markup.add(button1, button2,button3,button4)

          bot.reply_to(message, "Hosgeldiniz!!", reply_markup=admin_markup)
        else:
          bot.reply_to(message, "SyntaxError")

  except SyntaxError:
      bot.reply_to(message, "Sertifikat kodyny girizmekde yalnyshlyk!")



    





def password_step(message):
  try:
      user_id = message.from_user.id
      parol = message.text
      cursor = db.cursor()
      cursor.execute("SELECT investor_id, type_id FROM tbl_investors WHERE investor_password = '" + str(parol) + "'")
      f = cursor.fetchall()
      investor_ids = f[0]
      print(investor_ids)
      print(investor_ids[0])
      user_data.append(investor_ids[0])
      user_data.append(investor_ids[1])
      print("data added =>", user_data)

      if investor_ids is None:
        code_error = bot.send_message(message.chat.id, "Bagyslan shahsy kodynyz tapylmady! Kodynyzy gaytadan girin:")
        bot.register_next_step_handler(code_error, password_step)
      else:
        
        code_exit = bot.send_message(message.chat.id, "Congratulations! {0.first_name} Sertifikat kodynyzy girin:".format(message.from_user))
        bot.register_next_step_handler(code_exit, find_certificate_code)
  except SyntaxError:
      bot.reply_to(message, "Shahsy kodyny girizmekde yalnyshlyk!")













@bot.callback_query_handler(func=lambda call: True)
def callback(call, message):
  db = mysql.connector.connect(
            host="hasabym.com",
            user="u1184328_telegrm",
            passwd="telegram_db1",
            port="3306",
            database="u1184328_telegrm")
  
  
  if call.message:
    if call.data == 'img':
      cursor = db.cursor()
      cursor.execute('SELECT img_data FROM tbl_images')
      outputs = cursor.fetchone()

      for i in outputs:
        bot.send_photo(message.from_user.id, i)
        print(i)
    if call.data == 'ba':
      cursor = db.cursor()
      cursor.execute("SELECT sum(investment_amount) as investment_amount FROM tbl_investment WHERE investor_id = '" + str(user_data[0]) + "'")
      summa = cursor.fetchone()
      print("adawfaf", summa[0])
    else:
      bot.send_message(call.message.chat.id, "youasx balace")
  else:
    pass







bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
  bot.polling(none_stop=True)
    
    