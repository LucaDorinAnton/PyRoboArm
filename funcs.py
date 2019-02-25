from machine import Pin
from machine import ADC

import time
import network
import usocket
import sys
import struct
# This file provides all the necessary
# functions for your remote control

# Read through the comments if you are not sure
# what each function does


# The network object used to send data
wlan = network.WLAN(network.STA_IF)

# Connect to the network with the essid name
# This will either be ESP-Robot-ARM-1,
#  ESP-Robot-ARM-2 or ESP-Robot-ARM-3
# This function will try to connect to the network
# from scratch, by first disconnecting from any network
# It might be connected to and then trying to connect
# If the network is not available i.e. the arm you are
# trying to reach is turned off, this function
# will terminate your program
def connect(name):
  global wlan
  wlan.active(True)
  if wlan.isconnected():
    print("Disconnecting!")
    wlan.disconnect()
    wlan.active(False)
    wlan.active(True)
  found_it = False
  for net in wlan.scan():
    if net[0].decode('utf-8').strip() == name:
      found_it = True
  if not found_it:
    print("Network not available! Shutting down!")
    sys.exit(0)
  if wlan.isconnected():
    print("Connected!")
    print(wlan.ifconfig())
    print(wlan.config('essid'))
  else:
    print("Not connected!")
  while not wlan.isconnected():
    print("Trying to connect to network", n_name)
    wlan.connect(n_name)
    if wlan.isconnected():
      print("We have a connection!")
    else:
      print("I can't connect!")
    time.sleep_ms(1000)


# Define an output pin on the pin with the number p
# P should be in the following ranges:
# (12-14), (25-27), (32-35)
# This function returns a pin object
# which can be turned on or off using p.on() or p.off()
# When turned on, the pin will constantly output 3.3V
# If you want to check wether the pin is on or off,
# run p.value() . It will return either 0 for 'off'
# or 1 for 'on'
def pin_out(p):
    pin = Pin(p, Pin.OUT)
    return pin()


# Define an input pin on the pin with the number p
# P should be in the following ranges:
# (12-14), (25-27), (32-35)
# This function returns a pin object
# The value of the pin can be read by running p.value()
# If it is 0, the pin is not reading anything
# If it is 1, the pin is reading some input on it (meaning
# that your button is being pressed!)
def pin_in(p):
    pin = Pin(p, Pin.IN, Pin.PULL_DOWN)
    return pin

def pot(p):
    adc = ADC(Pin(p))
    adc.atten(ADC.ATTN_11DB)
    return adc

# Send a command to the robot arm
# The command should be 4 integers between 0 and 180 encapsulated
# In a list. For example send_cmd([0, 45, 90, 180])
# Each Integer represents the degree to which a certain servo
# should rotate to.
# The order for the values is as follows:
#  0 - right side servo
#  1 - left side servo
#  2 - bottom servo
#  3 - claw servo
# Make sure to normalise your values when calling this function!
# You should do this by calling the normalise_vals() function
# on your list!
# The values should be between 0 and 180 degrees, as the servos
# have only 180 degrees of rotational freedom.
def send_cmd(vals):
  try:
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    sock.connect(usocket.getaddrinfo("192.168.4.1", 1337)[0][-1])
    pkg = struct.pack("BBBB", vals[0], vals[1], vals[2], vals[3])
    sock.send(pkg)
    sock.close()
  except:
    print("Unable to send command! Resetting network...")
    connect()


# Normalise the values of a list.
# Take each element from the list and put it in a new list.
# If the element is either over 180 or under 0, set is
# as 180 or 0 respectiveley.
# Return the new list.
def normalise_vals(lst):
    res = []
    for i in lst:
        if i > 180:
            i = 180
        elif i < 0:
            i = 0;
        res.append(i)
    return res
