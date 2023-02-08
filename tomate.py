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
                os.system('play -nq -t alsa synth {} sine {}'.format(1, 264)) # tiempo y frecuencia
                os.system("notify-send -t 10000 \"Recreo cumplido\"")
            continue

def tomate(category):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    hms = now.strftime("%H:%M:%S")

    mins = 25

    os.system("bspc node -d '^9'")
    t = mins
    while t:
        limpiar()
        print(f"Estás en Tomate, quedan {t} minutos")#, end="\r")
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

    os.system('play -nq -t alsa synth {} sine {}'.format(1, 440)) # tiempo y frecuencia
    os.system("notify-send -t 60000 \"Fin del tomate\"")
    os.system("polybar-msg hook tomato 1")
    descanso()

main = Menu("Categorías", [
    Menu("academic", [Action(i, lambda: tomate(i)) for i in ac]),
    Menu("extra academic", [Action(i, lambda: tomate(i)) for i in ex_ac])])
main.navigate()
