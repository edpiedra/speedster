#!/usr/bin/env python3

import board, busio, digitalio 
import adafruit_rfm9x 
import numpy as np
from l298n_motorcontroller import *

drive = L298N()

spi = busio.SPI( board.SCK, MOSI=board.MOSI, MISO=board.MISO )
CS = digitalio.DigitalInOut( board.CE1 )
RESET = digitalio.DigitalInOut( board.D5 )
RADIO_FREQ_MHZ = 915.0

rfm9x = adafruit_rfm9x.RFM9x( spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000 )
rfm9x.tx_power = 13 #default is 13 can go up to 23dB

while True:
    
    packet = rfm9x.receive()
    print(packet)
    
    rfm9x.send(bytes("ok", "utf-8"))
    
    if packet is not None:
        speeds = list(np.array(str(packet, "ascii").split("|"), dtype="float"))
        drive._set_direction( speeds[0], speeds[1] )