import time, neopixel, machine, network, ntptime, os
from time import sleep
import socket

but1 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
but2 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

n = [neopixel.NeoPixel(machine.Pin(15), 7),
    neopixel.NeoPixel(machine.Pin(13), 7),
    neopixel.NeoPixel(machine.Pin(12), 7),
    neopixel.NeoPixel(machine.Pin(14), 7),
    neopixel.NeoPixel(machine.Pin(10), 2)]#кортеж цифр

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
            sleep(0.1)
        return colors
    if brightness == '-':        
        for i in list(range(3)):
            colors[i] -= 25
            sleep(0.1)
        return colors
 

def sends():
    with open("test.txt", "w") as f:
        for col in colors:
            f.write(str(col)+'\n')

def startap(flags = True):
    wlan_id = "Watchs"
    wlan_pass = "hQVwkszd)"
    ap = network.WLAN(network.AP_IF)
    if flags == True:
        ap.active(flags)
        ap.config(essid = wlan_id, password = wlan_pass)
        print('Device IP:', ap.ifconfig()[0])
        for j in list(range(4)):
            for i in list(range(7)):
                n[j][i] = (0, 50, 50)
            n[j].write()
    elif flags == False:
        ap.active(flags)
      
def handle_http(client, client_addr):
    client.send("<div><span class='q l'></span></div>")
    client.send('<form method="get" action="wifisave"><input id="s" name="s" length="32" placeholder="SSID"><br><input id="p" name="p" length="64" type="password" placeholder="password"><br><br><button type="submit">save</button></form>')
    client.close()

def serv():
    startap()
    http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http.bind((('', 80)))
    http.listen(10)
    client, client_addr = http.accept()
    handle_http(client, client_addr)
    while True:
        conn, addr = http.accept()
        print('Сайт создан')
        for j in list(range(4)):
            for i in list(range(7)):
                n[j][i] = (0, 0, 50)
            n[j].write()
        request = conn.recv(1024)
        request = str(request)
        if request.find('GET /wifisave?s=') > 0:
            x = request.find("/wifisave?s=")
            y = request.find("&p=")
            wlan_id = request[x+12:y]
            x = request.find("&p=")
            y = request.find(" HTTP")
            wlan_pass = request[x+3:y]
            with open("network.txt", "w") as w:
                w.write(wlan_id + '\n')
                print('SSID ok ' + wlan_id)
                w.write(wlan_pass)
                print('PASS ok ' + wlan_pass)
            startap(False)
            conn.close()
            startwlan(wlan_id, wlan_pass)
            
def opens(indexs = 2):
    if indexs == 1:
        with open("test.txt", "r") as f:
            col = f.readlines()
            return col
    if indexs == 2:
        with open("network.txt", "r") as r:
            text = r.readlines()
            sleep(1)
            if text not in []:
                ids = text[0]
                wlan_id = ids[:-1]
                wlan_pass = text[1]
                print(wlan_id)
                print(wlan_pass)
                startwlan(wlan_id, wlan_pass)
            else:
                serv()

def startwlan(wlan_id, wlan_pass):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected() == False:
        wlan.connect(wlan_id, wlan_pass)
        time.sleep(1)
        while wlan.isconnected() == False:
            serv()
#     wlan.connect(wlan_id, wlan_pass)
    print('Device IP:', wlan.ifconfig())
    for j in list(range(4)):
        for i in list(range(7)):
            n[j][i] = (0, 50, 0)
            n[j].write()
    start()
    
palit = opens(1)
colors = [int(palit[0]), int(palit[1]), int(palit[2])]



def start():
    mm = 66
    while True:
        if but1.value() == 1 and but2.value() == 1:
            ntptime.settime()
        dt_now = time.localtime()
        if dt_now[4] != mm or but1.value() == 1 or but2.value() == 1:
            if but1.value() == 1 and colors != [250, 250, 250]:
                color('+')
                sends()
            if but2.value() == 1 and colors != [0, 0, 0]:
                color('-')
                sends()
            hh, mm = dt_now[3]+3, dt_now[4]
            if hh > 23:
                hh = hh - 24
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

opens()     
