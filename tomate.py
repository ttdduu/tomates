#!/usr/bin/env python3

import time
import os
import json
from datetime import datetime
import string
from menu import *
from inputimeout import inputimeout, TimeoutOccurred
from categorias_tomates import academic as ac
from categorias_tomates import extra_academic as ex_ac
from motivation import frases as frases

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

# bh_folder = os.environ.get("brainhub_folder")
home = os.environ.get('HOME')
dir_path = home
def cargar():
    global registro
    with open(f'{dir_path}/log_tomates.json') as json_registro:
        registro = json.load(json_registro)

def guardar():
    with open(f'{dir_path}/log_tomates.json', 'w', encoding='utf-8') as reg:
        json.dump(registro, reg, ensure_ascii=False)

def gyc():
    guardar()
    cargar()

cargar()
limpiar()

def descanso():
    #  t=0
    # os.system('play -nq -t alsa synth {} sine {}'.format(2, 236)) # tiempo y frecuencia
    t=0
    while True:
        limpiar()
        print(f"En descanso hace {t//60} minutos {t%60} segundos")
        t += 1
        try:
            something = inputimeout(prompt="Apretar enter para terminar descanso", timeout=1)
            main.navigate()
        except TimeoutOccurred:
            if t >= 5*60 and t%30==0:
                t +=1
                # os.system('play -nq -t alsa synth {} sine {} gain 0.5'.format(1, 241)) # tiempo y frecuencia
                os.system("notify-send -t 10000 \"Recreo cumplido\"")
            continue


def sound(t,freq):
    sonido = os.system('play -nq -t alsa synth {} sine {} norm -1 gain -20'.format(t, freq))
    return sonido

def notif_sound():
    sound(3,100)
    sound(3,150)
    sound(1,350)
    sound(1,400)
    sound(1,500)

def tomate(category):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    hms = now.strftime("%H:%M:%S")

    mins = 25

    os.system("bspc node -d '^9'")
    t = mins
    while t:
        limpiar()
        print(f"Estás en Tomate, quedan {t} minutos,\n{frases[1]}")
        time.sleep(60)
        t -= 1
    if date in registro.keys():
        if category in registro[date].keys():
            registro[date][category]+= 1
        else:
            registro[date][category] = 1
    else:
        registro[date] = {category: 1}
    guardar()
    limpiar()

    notif_sound()
    os.system("notify-send -t 60000 \"Fin del tomate\"")
    os.system("polybar-msg hook tomato 1")
    os.system('dropbox start')
    descanso()

# lista_ac = [Action(i, lambda: tomate(i)) for i in ac]
# lista_ex_ac = [Action(i, lambda: tomate(i)) for i in ex_ac]
main = Menu("Categorías", [
    Menu(
        "academic",
        [
        Action(ac[0], lambda: tomate(ac[0])),
        Action(ac[1], lambda: tomate(ac[1])),
        Action(ac[2], lambda: tomate(ac[2])),
        Action(ac[3], lambda: tomate(ac[3])),
        Action(ac[4], lambda: tomate(ac[4]))
        ]),
    Menu("extra academic",
        [
        Action(ex_ac[0], lambda: tomate(ex_ac[0])),
        Action(ex_ac[1], lambda: tomate(ex_ac[1])),
        Action(ex_ac[2], lambda: tomate(ex_ac[2]))
        ])])


main.navigate()
