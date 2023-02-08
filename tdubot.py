#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import os
import time
from datetime import datetime
from datetime import timedelta
import json
from categorias_tomates import academic as ac
from categorias_tomates import extra_academic as ex_ac

token = '5843649088:AAGzlivbRewGy6opGMLgCACucz_hKJevBlQ'
bot = telebot.TeleBot(token)

home = os.environ.get('HOME')
log_comandos_dir = f'{home}/log_telegram.txt'
log_tomates_dir = f'{home}/log_tomates.json'

whitelist = [865644126]

# {{{ comandos

# {{{ start
@bot.message_handler(commands=['start'])
def command_long_text(m):
    cid = m.chat.id
    if cid not in whitelist:
        bot.send_message(cid,'es un bot privado, por favor no interferir')
        bot.send_message(cid,f'{cid}')
        return
    else:
        bot.send_message(cid,'funcionó carajo! confirmo!!!!')
# }}}

# {{{ exec

@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    if cid not in whitelist:
        # bot.send_message(cid,'es un bot privado, por favor no interferir')
        return
    else:
        bot.send_message(cid, "Ejecutando: " + m.text[len("/exec"):])
        f = os.popen(m.text[len("/exec "):])
        result = f.read()
        bot.send_message(cid,"Resultado: " +result, reply_markup=markup)
# }}}

# {{{ execlist

@bot.message_handler(commands=['execlist'])
def command_long_text(m):
    cid = m.chat.id
    if cid not in whitelist:
        # bot.send_message(cid,'es un bot privado, por favor no interferir')
        return
    else:
        comandos = m.text[len("/execlist\n"):].split('\n')
        for com in comandos:
            bot.send_message(cid, "Ejecutando: " + com)
            bot.send_chat_action(cid, 'typing') # acción "escribiendo"
            time.sleep(2)
            f = os.popen(com)
            result = f.read()
            bot.send_message(cid, "Resultado: " + result, )
        bot.send_message(cid,"Comandos ejecutados", reply_markup=markup)
# }}}

# {{{ cd

@bot.message_handler(commands=['cd'])
def command_long_text(m):
    cid = m.chat.id
    if cid not in whitelist:
        # bot.send_message(cid,'es un bot privado, por favor no interferir')
        return
    else:
        bot.send_message(cid,"Cambio a directorio:"+m.text[len("/cd"):])
        bot.send_chat_action(cid, 'typing') # acción "escribiendo"
        time.sleep(2)
        os.chdir(m.text[len("/cd"):].strip())
        f = os.popen("pwd")
        result = f.read()
        bot.send_message(cid,"Directorio :"+result, reply_markup=markup)
# }}}


commands = {
        'tomate': 'registrar un tomate',
        'exec': 'ejecutar un comando',
        'cd': 'cambiar de directorio',
        'execlist': 'ejectuar lista de comandos'
        }

# {{{ reply keyboard

markup = types.ReplyKeyboardMarkup()

markup.row('/tomate','/energia','/atencion','/spm')
markup.row('/social','/creatina','/ducha','/pos')

markup.row('/ithink','/reg','/imp')

markup.row('/sadtencion','/brainweak','/braindead')
markup.row('/cringe','/freeze','/block','/ans')

markup.row('/sadsocial','/lumbar','/nails')
markup.row('/error','/obstaculo','/fatiga')

markup.row('/gracias','/lindo','/dream')
# }}}

# {{{ consecuencia
@bot.message_handler(commands=['braindead','freeze','block','fatiga','nails','lumbar','error'])
def consecuencia(m):
    cid = m.chat.id
    if cid not in whitelist:
        bot.send_message(cid,'es un bot privado, por favor no interferir')
        bot.send_message(cid,f'{cid}')
        return
    else:
        os.system('echo {} > /home/tdu/Dropbox/log_tomates.json')
        bot.send_message(cid,'borrón y cuenta nueva. Estoy imponiéndome esta consecuencia porque sé que puedo. Quiero mejorar definitivamente. Es el momento de crecer y ser mucho, mucho mejor.')
# }}}

# {{{ restart

@bot.message_handler(commands=['restart'])
def apagar(m):
    cid = m.chat.id
    if cid not in whitelist:
        bot.send_message(cid,'es un bot privado, por favor no interferir')
        bot.send_message(cid,f'{cid}')
        return
    else:
        os.system('cd /home/tdu/code/tomates && git pull origin main')
        os.system("pid=$(ps -ef | grep tdubot | awk '{print $2}' | head -n 1 | awk '{match($0,/[0-9]+/); print substr($0,RSTART,RLENGTH)}') && kill $pid && st -e tdubot.py")
# }}}

# }}}

# {{{ tomate

def cargar():
    global registro
    with open(log_tomates_dir) as json_registro:
        registro = json.load(json_registro)

def guardar():
    with open(log_tomates_dir, 'w', encoding='utf-8') as reg:
        json.dump(registro, reg, ensure_ascii=False)

def markup_inline():
    in_markup = types.InlineKeyboardMarkup()
    in_markup.width = 2
    for i in ac+ex_ac:
        in_markup.add(
                types.InlineKeyboardButton(str(i), callback_data= i)
                )
    return in_markup

def tomates_hechos(fecha):
    if fecha in registro.keys():
        return registro[fecha]
    else:
        return 0

@bot.message_handler(commands=['tomate'])
def hola(msj):
    cargar()
    fecha_tomate = datetime.fromtimestamp(msj.json['date'])
    global date
    date = fecha_tomate.strftime('%d/%m/%Y')
    bot.reply_to(msj, f'tomates de hoy {date}: \n{tomates_hechos(date)}', reply_markup = markup_inline())

@bot.callback_query_handler(func = lambda m: True)
def callback_query(call):
    bot.answer_callback_query(call.id, f'registré un tomate de {call.data}')
    global category
    category = call.data
    sumar_tomate()

# sumar un tomate. syntax: /+1 category
@bot.message_handler(commands=['tomate'])
def sumar_tomate():
    if date in registro.keys():
        if category in registro[date].keys():
            registro[date][category]+= 1
        else:
            registro[date][category] = 1
    else:
        registro[date] = {category: 1}
    guardar()
    '''lo hago sin hms xq no es relevante la info de cuándo hago cada tomate'''
    os.system('dropbox start')

# }}}

# main
if __name__ == '__main__':
    print('iniciando el bot')
    bot.infinity_polling() #es infinite loop para ver si hay msj nuevo
