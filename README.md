# acm
Automatic Coffee Maker (ACM) attachment for the Mr. Coffee, 5-Cup Mini Brew Switch Coffee Maker

ME100 (Electronics for the Internet of Things) Final Project
Fall 2022

# Notable Disciplines
ESP32, MicroPython, SolidWorks, 3D Printing, Adafruit/MQTT

# Synopsis
The automatic coffee maker (ACM) is a modular attachment to the Mr. Coffee 5-Brew Mini Switch that uses a microcontroller board and a servo motor to control the heating element and temperature of the coffee. The ACM connects to a WiFi network and communicates with the Adafruit server to receive updates on the status of the coffee and to send updates on the coffee's temperature.

The ACM has a button and two LEDs, one green and one red, that are used to signal the status of the coffee. The green LED is turned on when the coffee is brewing, and the red LED is turned on when the coffee is ready. The button can be used to manually turn off the heating element.

To use the ACM, the user first sets the desired brewing temperature using the Adafruit server. The ACM then heats the coffee until it reaches the desired temperature and begins brewing. When the coffee is brewed, the ACM begins monitoring the temperature and sends updates to the Adafruit server with the current temperature rate of change. When the temperature falls below a certain threshold, the ACM switches off the heating element and indicates that the coffee is ready.

The ACM is powered by a microcontroller board and uses a servo motor to control the heating element. The temperature is measured using an ADC on pin 34. The button and LEDs are connected to pins 13, 27, and 12, respectively, and the servo is connected to pin 33. The ACM communicates with the Adafruit server over the MQTT protocol on port 1883.

The housing of the ACM has been 3D printed and modeled using SolidWorks and tight dimensioning in order to fit the microcontroller and servo motors snugly. It is attached to the machine by the underside of the Mr. Coffee maker.

# Motivations
This project was made under the guidance of UC Berkeley’s ME100 final project for the course, Electronics for the Internet of Things. It required us to incorporate an actuator (servo motor) and sensor (thermocouple) into an ESP32, along with additional parts such as LEDs and buttons to make the project work.

# Learning Process and Challenges
This project challenged what I have learned over the course of taking ME100. It exposed me to the fundamentals of circuitry and electronics, how it can be used to communicate with other devices (IOT) using MQTT protocols and Adafruit, CADD (SolidWorks), and 3D Printing and its respective challenges of tolerancing. I’ve been able to understand the simple processes and theories of circuits and their respective parts, such as capacitors, diodes, inductors, and other complements to circuits. This project challenged my understanding of these circuits and communication through the ESP32 using MicroPython. 

Several challenges appeared during this project:
Deciding how to activate the physical manual switch of the coffee maker, since I did not want to tamper with this original product
How to interpret the data of the thermocouple data using a formula

Solutions in its respective order:
Installed a servo motor between a rotatable 3D printed attachment to the switch using a double sided adhesive
Modeled the ACM housing to be installed to the nubs on the underside of the Mr. Coffee original product to prevent any slip or pushback whenever the servo motor moves
Searched online to discover a formula that interprets the data to Celsius/Fahrenheit, human readable data

