import time, neopixel, machine, os
from machine import Pin
from time import sleep

mm = 66

but1 = Pin(4, Pin.IN, Pin.PULL_UP)
but2 = Pin(5, Pin.IN, Pin.PULL_UP)

n = [neopixel.NeoPixel(machine.Pin(15), 7),
    neopixel.NeoPixel(machine.Pin(13), 7),
    neopixel.NeoPixel(machine.Pin(12), 7),
    neopixel.NeoPixel(machine.Pin(14), 7),
    neopixel.NeoPixel(machine.Pin(10), 2)]

#кортеж цифр
digits = [
    [1,1,1,0,1,1,1],# Цифра 0
    [0,0,1,0,0,0,1],# Цифра 1
    [1,1,0,1,0,1,1],# Цифра 2
    [0,1,1,1,0,1,1],# Цифра 3
    [0,0,1,1,1,0,1],# Цифра 4
    [0,1,1,1,1,1,0],# Цифра 5
    [1,1,1,1,1,1,0],# Цифра 6
    [0,0,1,0,0,1,1],# Цифра 7
    [1,1,1,1,1,1,1],# Цифра 8
    [0,1,1,1,1,1,1] # Цифра 9
    ]

def clean(a):
    for i in list(range(7)):
        n[a][i] = (0, 0, 0)
    n[a].write()
    
def seconds():
    dt_ss = time.localtime()
    if dt_ss[5] % 2 == 0 or dt_ss[5] == 0:
        for i in list(range(2)):
            n[4][i] = colors
    else:
        for i in list(range(2)):
            n[4][i] = (0, 0, 0)
    n[4].write()
        
def color(brightness=0):
    if brightness == '+':            
        for i in list(range(3)):
            colors[i] += 25
        return colors
    if brightness == '-':        
        for i in list(range(3)):
            colors[i] -= 25
        return colors
    
def sends():
    with open("test.txt", "w") as f:
        for col in colors:
            f.write(str(col)+'\n')
            
def opens():
    with open("test.txt", "r") as f:
        col = f.readlines()
        return col
        
palit = opens()
colors = [int(palit[0]), int(palit[1]), int(palit[2])]
    
while True:
    dt_now = time.localtime()
    if dt_now[4] != mm or but1.value() == 1 or but2.value() == 1:
        if but1.value() == 1 and colors != [250, 250, 250]:
            color('+')
            sends()
        if but2.value() == 1 and colors != [0, 0, 0]:
            color('-')
            sends()
        hh, mm = dt_now[3], dt_now[4]
        print('Сейчас '+str(hh)+' часов '+str(mm)+' минуты')
        w = [hh // 10, hh % 10, #Разделяем часы на однозначные числа
            mm // 10, mm % 10] #Разделяем минуты на однозначные числа
        for j in list(range(4)):
            clean(j)
            for i in list(range(7)):
                digit = digits[w[j]][i]
                if digit == 1:
                    n[j][i] = colors
                    n[j].write()
    seconds()
        
