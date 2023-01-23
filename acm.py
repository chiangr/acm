# Import necessary libraries

from board import LED
from machine import Pin, PWM, Timer, ADC
from time import sleep
import math

from mqttclient import MQTTClient
import network
import sys
import time

# Check wifi connection

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection

adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'rychi'
adafruitAioKey = 'aio_CtFV52qM86i0SFksxGQoos4vAv9J'

# Callback function when MQTT message is received

def sub_cb(topic, msg):
    global press_request
    global disable
    if msg == b'1':
        press_request = True
        disable = True
    else:
        press_request = False
    # print(topic,msg)

# Connect to Adafruit server

print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

mqtt.set_callback(sub_cb)

switch_feed = "rychi/feeds/acm.switch"
mqtt.subscribe(switch_feed)

temp_feed = "rychi/feeds/acm.temperature"
mqtt.subscribe(temp_feed)

# Initialize pins to its respective loads

button = Pin(13, mode=Pin.IN)
led_g = Pin(27, mode=Pin.OUT)
led_r = Pin(12, mode=Pin.OUT)
servo = PWM(Pin(33), freq=50)

therm = ADC(Pin(34))
therm.atten(ADC.ATTN_6DB)

servo_status = True
disable = False


# Start the automatic coffee maker
# When the coffee brews, it will recognize when the coffee exceeds 140 degrees
# Allows the user to keep it on OR turn coffee maker off
# Relays temperature value in Fahrenheit to the terminal and MQTT
# Reach temperature values and send updates to user

def start_acm():

    global disable

    temp_cache = []
    complete = False

    get_temperature()
    # print("Please allow 30 seconds to elapse.")

    # sleep(30)

    pre_threshold = 140

    while get_temperature() < pre_threshold:
        print("\n! Heating... Waiting for temperature to reach above %.2f F\n" %(pre_threshold))
        sleep(0)

    print("Please allow 1 minute to pass to let the coffee brew.")
    sleep(60)

    print("> Temperature has exceeded %.2f F and has been brewed." %(pre_threshold))
    mqtt.publish(switch_feed,"> Temperature has reached %.2f F and has been brewed." %(pre_threshold))

    temp_cache.append(get_temperature())

    counter = 0

    brewing_chk = True
    perfect_temp_chk = True

    print("\n > Coffee in Progress ...")
    print("\nTip: Hold down the button or use IFTTT to turn off the heat OR Keep it heated by keeping it on")
    
    disable = False

    while not(disable):
        disable = button.value()
        mqtt.check_msg()
        print("...")
        sleep(.5)
        if disable:
            switch()

    while not(complete):

        print("Cooling down the Coffee. We will give you updates on when it is ready!")

        temp_cache.append(get_temperature())

        temp_rate = (temp_cache[len(temp_cache)-1]-temp_cache[len(temp_cache)-2])/(10)
        print("Your Coffee is cooling at a rate of %.2f F/s" %(temp_rate*-1))

        avg_temp = (temp_cache[len(temp_cache)-1]+temp_cache[len(temp_cache)-2]+temp_cache[len(temp_cache)-3])/3


        if avg_temp <= 100:
            mqtt.publish(switch_feed,"Turning off ACM as temperature is below 100. Warm up your coffee or drink it cold!")
            print("Turning off ACM as temperature is below 100. Warm up your coffee or drink it cold!")
            complete = True
        elif avg_temp <= 140 and perfect_temp_chk:
            perfect_temp_chk = False
            mqtt.publish(switch_feed,"Your coffee is at the perfect temperature of about %.2f F!" %(avg_temp))
            print("Your coffee is at the perfect temperature of about %.2f F!" %(avg_temp))
        elif temp_rate < 0 and brewing_chk:
            if counter == 3:
                brewing_chk = False
                mqtt.publish(switch_feed,"Your coffee is getting colder...")
                print("Your coffee is getting colder...")
            else:
                if counter == 0:
                    counter += 1
                else:
                    counter = 0


# Gets the temperature from thermocouple and converts data to Fahrenheit

def get_temperature():

    temp_list = []

    for l in range(10):

        therm_reading = []
        therm_sum = 0.0

        for k in range(10):
            therm_reading.append(therm.read())
            therm_sum += therm_reading[k]

        temp_avg = (((therm_sum/10000)-1.25)/0.005 + 1.00)*(9/5)+32
        temp_list.append(temp_avg)

        sleep(1)
    for i in range(5):
        temp_list.remove(max(temp_list))
    temp_whole_avg = sum(temp_list)/len(temp_list)
    mqtt.publish(temp_feed,str(temp_whole_avg))
    print("> %.2f F" %(temp_whole_avg))
    return temp_whole_avg


# Toggle coffee maker on/off

def switch():
    global servo_status
    if servo_status:
        servo_status = False
        servo.duty(5)
        led_g.value(1)
        led_r.value(0)
        start_acm()
    else:
        servo_status = True
        servo.duty(8)
        led_r.value(1)
        led_g.value(0)

# Wait on trigger to start automatic coffee maker

servo.duty(8)
led_r.value(1)

while True:
    mqtt.check_msg()

    pressed = False
    press_request = False

    while not(pressed) and not(press_request):
        pressed = button.value()
        mqtt.check_msg()
        print("Waiting for Response...")
        sleep(.5)

    print("\n >> Initiating Automatic Coffee Maker \n")

    switch()