'''
Task control test with pyControl v1.5 with breakout board v1.2
Copyright (c) 2019, 2020 Yuichi Takeuchi
'''

from pyControl.utility import *
import hardware_definition as hw  # hw_GoNoGoTask_2v1.py

# -------------------------------------------------------------------------
# States and events.
# -------------------------------------------------------------------------
states = ['init_state']

events = ['blinker_on',		# pyboard LED on
          'blinker_off', 	# pyboard LED off
          'rsync']

initial_state = 'init_state'

# -------------------------------------------------------------------------
# Variables.
# -------------------------------------------------------------------------
# Parameters.
# Variables.
v.LED_n = 4  # Number of LED to use.


# Run start and stop behaviours.
def run_start():
    pyb.LED(v.LED_n).on()
    set_timer('blinker_off', 1*second)  # option: output_event=True


def run_end():
    pyb.LED(v.LED_n).off()
    hw.off()


# State & event dependent behaviours.
def init_state(event):
    # inital state
    if event == 'entry':
        hw.houselight1.on()
        hw.houselight2.on()
        hw.houselight3.on()
    elif event == 'exit':
        hw.houselight1.off()
        hw.houselight2.off()
        hw.houselight3.off()


# -------------------------------------------------------------------------
# State independent behaviour.
# -------------------------------------------------------------------------
def all_states(event):
    # Turn a LED on and off when the corrsponding timer trigger, set timer for next LED on/off.
    if event == 'blinker_on':
        pyb.LED(v.LED_n).on()
        set_timer('blinker_off', 1*second)  # option: output_event=True
    elif event == 'blinker_off':
        pyb.LED(v.LED_n).off()
        set_timer('blinker_on', 1*second)
