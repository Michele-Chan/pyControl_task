# demo

# Imports
from pyControl.utility import *
from devices import *
import hardware_definition as hw # hw_GoNoGoTask_2v1.py

# States and events.
states = ['LED_on',
          'LED_off']

events = ['button_press']

initial_state = 'LED_off'

# Variables.
v.LED_n  = 4 # Number of LED to use.

# Define behaviour

def LED_on(event):
    if event == 'entry':
        timed_goto_state('LED_off', 0.5 * second)
        pyb.LED(v.LED_n).on()
        #hw.speaker.sine(5000)
        #hw.speaker.noise()
        #hw.speaker.click()
        hw.speaker.click(500)
    elif event == 'exit':
        pyb.LED(v.LED_n).off()
        hw.speaker.off()
    elif event == 'button_press':
        goto_state('LED_off')

def LED_off(event):
    if event == 'entry':
        timed_goto_state('LED_on', 0.5 * second)
    elif event == 'button_press':
        goto_state('LED_on')


def run_end():  # Turn off hardware at end of run.
    pyb.LED(v.LED_n).off()
    hw.speaker.off()
