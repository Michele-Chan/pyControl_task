# Demo device setup

from devices import *

# Board difinition
board = Breakout_1_2()

# Instantiate Devices.
LED    = Digital_output(pin='X2')
#button = Digital_input(pin='X1', rising_event='button_press', falling_event='button_release')
pyboard_button = Digital_input('X17', falling_event='button_press', pull='up')  # USR button on pyboard.
speaker = Audio_board(board.port_3)

