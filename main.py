# DHT22 libray is available at
# https://github.com/danjperron/PicoDHT22
# esp8266_i2c_lcd libray is available at
# https://github.com/dhylands/python_lcd

import utime
from machine import I2C, Pin
from lib.esp8266_i2c_lcd import I2cLcd
from lib.DHT22 import DHT22

mode = 0

def main():
    # LCD
    DEFAULT_I2C_ADDR = 0x27
    i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    # Show boot message and wait 1 sec for DHT11 to be ready
    lcd.clear()
    lcd.backlight_on()
    lcd.putstr("Starting...")
    utime.sleep(1)

    # DHT 11
    dht_sensor = DHT22(Pin(13, Pin.OUT, Pin.PULL_DOWN), dht11=True)

    # Buttons
    but_mode = Pin(14, Pin.IN, Pin.PULL_DOWN)
    but_mode.irq(trigger=machine.Pin.IRQ_RISING, handler=switch_mode)

    temp_min = 0
    temp_max = temp_min
    hum_min = 0
    hum_max = hum_min

    while True:
        temp, hum = dht_sensor.read()
        if temp is None:
            print("DHT11 read error")
        else:
            if temp < temp_min or temp_min == 0:
                temp_min = temp
            if temp > temp_max or temp_max == 0:
                temp_max = temp
                
            if hum < hum_min or hum_min == 0:
                hum_min = hum
            if hum > hum_max or hum_max == 0:
                hum_max = hum
    
        if mode == 0:
            display_data(lcd, temp, hum)
        else:
            display_min_max(lcd, temp_min, temp_max, hum_min, hum_max)
        utime.sleep(1)
    
def display_data(lcd, temperature,  humidity):
    lcd.clear()
    lcd.putstr("Temperature " + str(temperature)+" C\nHumidity    " + str(humidity) + " %")

def display_min_max(lcd, temp_min, temp_max, hum_min, hum_max):
    lcd.clear()
    lcd.putstr("Temp " + str(temp_min) + " - " + str(temp_max) + " C")
    lcd.move_to(0, 1)
    lcd.putstr("Hum  " + str(hum_min) + " - " + str(hum_max) + " %")


def switch_mode(pin):
    global mode
    mode = (mode + 1) % 2
    print("Mode switched: " + str(mode))

if __name__ == '__main__':
    main()