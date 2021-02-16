import utime
from machine import I2C, Pin
from lib.esp8266_i2c_lcd import I2cLcd
from lib.dht import DHT11, InvalidChecksum

def main():
    # LCD
    DEFAULT_I2C_ADDR = 0x27
    i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    # Show boot message and wait 1 sec for DHT11 to be ready
    lcd.clear()
    lcd.putstr("Starting...")
    utime.sleep(1)

    # Internal temperature sensor
    internal_temp = machine.ADC(4)
    conversion_factor = 3.3 / 65535

    # DHT 11
    dht_sensor = DHT11(Pin(15, Pin.OUT, Pin.PULL_DOWN))

    while True:
        temp1 = internal_temp.read_u16() * conversion_factor
        temp1 = 27 - (temp1 - 0.706) / 0.001721
        
        temp2 = dht_sensor.temperature
        hum = dht_sensor.humidity
        
        display(lcd, temp1, temp2, hum)
        utime.sleep(1)
    
def display(lcd, temperature1, temperature2, humidity):
    lcd.clear()
    lcd.putstr("T1=" + str(round(temperature1, 1))+"\nT2=" + str(round(temperature2, 1)) + " H=" + str(round(humidity, 1)))

if __name__ == '__main__':
    main()