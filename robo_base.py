from machine import Pin
from machine import ADC
import time

from funcs import connect
from funcs import pin_out
from funcs import pin_in
from funcs import pot
from funcs import noralise_vals

# IMPORTANT NOTE:
# Working with hardware can be very buggy!
# If things go wrong, make sure you have saved your code
# then unplug and plug your boards back in your
# This should fix most of your problems!


# make sure to set the right number for
# the arm you are trying to connect to
n_name = 'ESP-Robot-ARM-x'

# declare your input and output pins
# and your potentiometers here


# declare a list storing the values for the servos
# list of 4 ints


def main():
  # connect to the network

  while True: #Loop forever
    # poll your input pins using .value()
    # or your potentiometers using .read()

    # adjust the values in your list accordingly
    # make sure to normalise your list!

    # use send_cmd(lst_name) to send your values
    # to the arm

    # don't remove this sleep functio.
    # If you do, your board will freeze and then crash
    # The arms are polling every 50ms for your commands anyway
    time.sleep_ms(50)

# DO NOT WRITE ANY CODE BELLOW THIS LINE

# Run the main function
main()
