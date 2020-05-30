'''
Solenoid valve manipulation (poke2)

Hardware definition file: hw_GoNoGoTask_2v1.py
Task control test with pyControl v1.5 with breakout board v1.2
Copyright (c) 2019, 2020 Yuichi Takeuchi
'''

from pyControl.utility import *
import hardware_definition as hw # hw_GoNoGoTask_2v1.py

#-------------------------------------------------------------------------
# States and events.
#-------------------------------------------------------------------------
states = ['init_state',
          'sol_off',
          'sol_on']

events = ['button_press', 	# USR button pressed
          'blinker_on',		# pyboard LED on
          'blinker_off', 	# pyboard LED off
          'session_timer',
          'rsync']

initial_state = 'init_state'

#-------------------------------------------------------------------------
# Variables.
#-------------------------------------------------------------------------
# Parameters.
v.LED_n  = 4 # Number of LED to use.
v.session_duration = 1     # Session duration in hour

#-------------------------------------------------------------------------        
# State machine code.
#-------------------------------------------------------------------------
# Run start and stop behaviours.
def run_start():
    pyb.LED(v.LED_n).on()
    hw.houselight1.on()
    hw.houselight2.on()
    hw.houselight3.on()
    hw.poke2.LED.on()
    set_timer('blinker_off', 1*second) # option: output_event=True
    set_timer('session_timer', v.session_duration*hour) 

def run_end():
    pyb.LED(v.LED_n).off()
    hw.off()

# State & event dependent behaviours.

def init_state(event):
    # inital state
    if event == 'entry':
        print('initialized')
    elif event == 'exit':
        pass
    elif event == 'button_press':
        goto('sol_off')

def sol_off(event):
    # close solenoid valve of poke2
    if event == 'entry':
    	hw.poke2.SOL.off()
    elif event == 'button_press':
        goto('sol_on')

def sol_on(event):
    # open solenoid valve of poke2
    if event == 'entry':
        hw.poke2.SOL.on()
    elif event == 'button_press':
        goto('sol_off')

#-------------------------------------------------------------------------
# State independent behaviour.
#-------------------------------------------------------------------------

def all_states(event):
    # Turn a LED on and off when the corrsponding timer trigger, set timer for next LED on/off.
    if event == 'blinker_on':
        pyb.LED(v.LED_n).on()
        set_timer('blinker_off', 1*second) # option: output_event=True
    elif event == 'blinker_off':
        pyb.LED(v.LED_n).off()
        set_timer('blinker_on' , 1*second)
    elif event == 'session_timer':  #session timer for framework
        stop_framework()
