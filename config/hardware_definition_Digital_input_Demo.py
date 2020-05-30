# Demo device setup

from devices import *

# Instantiate Devices.
button = Digital_input(pin='X1', rising_event='button_press', falling_event='button_release')
LED    = Digital_output(pin='X2')

