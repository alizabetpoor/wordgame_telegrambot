import telebot
from telebot import types
import databaseword
import random

API_TOKEN = '1190660423:AAGZXBmCMdmKmvi0T6dyWR8WSi_lH_88jbM'

bot = telebot.TeleBot(API_TOKEN)
print("bot is ready to use")


#start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        chat_id= message.chat.id
        chat_id=str(chat_id)
        databaseword.creatdatabase()
        databaseword.creatpersondatabase(chat_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('yes☑️')
        markup.add('cancel🔴')
        msg = bot.reply_to(message, 'do you want to start the game?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_word_step1)
    except:
        print("error in start")
        pass
myword=""
numberofallwords=1
def process_word_step1(message):
    try:
        global chat_id
        global myword
        global numberofallwords
        text=message.text
        text=text.lower()
        hide=types.ReplyKeyboardRemove()
        chat_id= message.chat.id
        if text=="yes☑️":
            numberofallwords=databaseword.lenall()
            searchword()
            newword=[]
            for letter in myword:
                newword.append(letter)
            random.shuffle(newword)
            newwords=",".join(newword)
            msg=bot.reply_to(message,f"guess the word : {newwords}\n if you want to exit the game please enter /cancel",reply_markup=hide)
            bot.register_next_step_handler(msg, process_word_step2)
        elif text == "cancel🔴":
            bot.reply_to(message,"ok try again later!",reply_markup=hide)
        else:
            msg=bot.reply_to(message,"please enter one keyboard⚠️")
            bot.register_next_step_handler(msg,process_word_step1)
    except:
        bot.reply_to(message,"no word exist",reply_markup=hide)
def process_word_step2(message):
    try:
        global myword
        text=message.text
        text=text.lower()
        if text==myword:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('yes☑️')
            markup.add('no🔴')
            msg=bot.reply_to(message,"your word is right✅. do you want to continue?",reply_markup=markup)
            databaseword.addperson(chat_id,myword)
            bot.register_next_step_handler(msg,nextstep)
        elif text=="/cancel":
            bot.reply_to(message,"you exit the game❌")
        else:
            msg=bot.reply_to(message,"your word is wrong,please try again⚠️")
            bot.register_next_step_handler(msg,process_word_step2)
    except:
        print("error in process_word_step2")
        pass
def nextstep(message):
    try:
        global myword
        global chat_id
        global numberofallwords
        text=message.text
        text=text.lower()
        hide=types.ReplyKeyboardRemove()
        if text=='yes☑️':
            numberofallwords=databaseword.lenall()
            searchword()
            newword=[]
            for letter in myword:
                newword.append(letter)
            random.shuffle(newword)
            newwords=",".join(newword)
            msg=bot.reply_to(message,f"guess the word : {newwords}\n if you want to exit the game please enter /cancel",reply_markup=hide)
            bot.register_next_step_handler(msg, process_word_step2)
        elif text=='no🔴':
            bot.reply_to(message,"ok⚠️",reply_markup=hide)
        else:
            bot.reply_to(message,"please choose one keyboard⚠️")
    except:
        print("error in next step")
        pass
#admin command
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    try:
        chat_id = message.chat.id
        myid=344254169
        if chat_id==myid:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=2)
            markup.add('add word','delete word','show all words')
            msg=bot.reply_to(message,"you have access",reply_markup=markup)
            bot.register_next_step_handler(msg,process_admin_panel)
        else:
            bot.reply_to(message,"access denid🚫")
    except:
        print("error in admin panel")
        pass
def process_admin_panel(message):
    try:
        text=message.text
        text=text.lower()
        hide=types.ReplyKeyboardRemove()
        if text=="add word":
            markup = types.ForceReply(selective=False)
            msg=bot.reply_to(message,"give me your word: ",reply_markup=markup)
            bot.register_next_step_handler(msg,add_word_proccess)
        elif text=="delete word":
            markup = types.ForceReply(selective=False)
            msg=bot.reply_to(message,"give me your word: ",reply_markup=markup)
            bot.register_next_step_handler(msg,delete_word_proccess)
        elif text=="show all words":
            tedad=databaseword.lenall()
            matn=""
            for i in range(0,tedad):
                idmatn=databaseword.showallwords()[i][0]
                idmatn=str(idmatn)
                matn+="✅"+idmatn+"-"+databaseword.showallwords()[i][1]
                matn+="\n"
            bot.reply_to(message,f"{matn}",reply_markup=hide)
        else:
            bot.reply_to(message,"your command doesn't found⚠️",reply_markup=hide)
    except:
        print("error in process_admin_panel")
        pass
def add_word_proccess(message):
    try:
        hide=types.ReplyKeyboardRemove()
        text=message.text
        text=text.lower()
        databaseword.add(text)
        bot.reply_to(message,f"{text} added to database successfully✅",reply_markup=hide)
    except:
        print("error in add_word_proccess")
        pass
def delete_word_proccess(message):
    try:
        hide=types.ReplyKeyboardRemove()
        text=message.text
        text=text.lower()
        #delete more than one word and use like this:ali,mohammad,hossein
        if "," in text:
            words=text.split(",")
            for word in words:
                condition=databaseword.remove(word)
                if condition==True:
                    bot.reply_to(message,"your word was deleted✅",reply_markup=hide)
                elif condition==False:
                    bot.reply_to(message,"your word was not found⚠️",reply_markup=hide)
        else:
            condition=databaseword.remove(text)
            if condition==True:
                bot.reply_to(message,"your word was deleted✅",reply_markup=hide)
            elif condition==False:
                bot.reply_to(message,"your word was not found⚠️",reply_markup=hide)
    except:
        print("error in delete_word_proccess")
        pass
def searchword():
    global numberofallwords
    global chat_id
    global myword
    chat_id=str(chat_id)
    randnumber=random.randint(1,numberofallwords)
    myword=databaseword.searchbyid(randnumber)
    if databaseword.findwordperson(chat_id,myword)==True:
        searchword()
    elif databaseword.findwordperson(chat_id,myword)==False:
        return myword
#setting command
@bot.message_handler(commands=['setting'])
def setting(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('clear your database☑️')
        markup.add('exit')
        msg = bot.reply_to(message, 'setting:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_setting_step)
    except:
        print("error in setting")
def process_setting_step(message):
    try:
        text=message.text
        text =text.lower()
        hide=types.ReplyKeyboardRemove()
        if text == 'clear your database☑️':
            chat_id=message.chat.id
            chat_id=str(chat_id)
            remove=databaseword.removepersondatabase(chat_id)
            if remove==True:
                bot.reply_to(message,"database deleted successfully!",reply_markup=hide)
            elif remove==False:
                bot.reply_to(message,"database is empty",reply_markup=hide)
        elif text == 'exit':
            bot.reply_to(message,"you exit the setting",reply_markup=hide)
        else:
            msg=bot.reply_to(message,"use one keyboard")
            bot.register_next_step_handler(msg,process_setting_step)
    except:
        print("error in process_setting_step")
        pass
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()