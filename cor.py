import lcddriver
import time
import http.client
import json
import os

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 0m5BDVJjfn7JPxMZS5azuV:7JebP4KUwsdvUCtRaqq06e"
    }

conn.request("GET", "/corona/totalData", headers=headers)

res = conn.getresponse()
data = res.read()

decoded = data.decode("utf-8")

new_data = json.loads(decoded)

totalCases = new_data['result']['totalCases']
totalDeaths = new_data['result']['totalDeaths']
totalRecovered = new_data['result']['totalRecovered']

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 0m5BDVJjfn7JPxMZS5azuV:7JebP4KUwsdvUCtRaqq06e"
    }

conn.request("GET", "/corona/countriesData", headers=headers)

res = conn.getresponse()
data = res.read()

decoded = data.decode("utf-8")

new_data = json.loads(decoded)

turnCount = 0

def foo(json_object, country):
    for dict in json_object:
        if dict['country'] == country:
            return dict['totalCases']

def long_string(display, text = '', num_line = 1, num_cols = 16):
    if(len(text) > num_cols):
        display.lcd_display_string(text[:num_cols],num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print,num_line)
            time.sleep(0.2)
        time.sleep(1)
    else:
	    display.lcd_display_string(text,num_line)

totalCasesTurkey = foo(new_data['result'], 'Turkey')

display = lcddriver.lcd()

try:
    while True:
        display.lcd_display_string("COVID-19 Cases", 1)
        time.sleep(2)
        display.lcd_clear()
        time.sleep(2)
        display.lcd_display_string("Worldwide", 1)
        display.lcd_display_string("C: %s" % totalCases, 2)
        time.sleep(3)
        display.lcd_display_string("D: %s" % totalDeaths, 2)
        time.sleep(3)
        display.lcd_display_string("R: %s" % totalRecovered, 2)
        time.sleep(2)
        display.lcd_clear()
        time.sleep(2)
        for obj in new_data['result']:
            long_string(display, obj['country'], 1)
            display.lcd_display_string("C: %s" % obj['totalCases'], 2)
            time.sleep(3)
            display.lcd_display_string("D: %s" % obj['totalDeaths'], 2)
            time.sleep(3)
            display.lcd_display_string("R: %s" % obj['totalRecovered'], 2)
            time.sleep(3)
            display.lcd_clear()
            time.sleep(2)
        turnCount += 1
        if(turnCount >= 2):
            break

except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()

os.system("python3 cor.py")