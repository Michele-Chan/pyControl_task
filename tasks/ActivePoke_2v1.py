'''
Task control test with pyControl v1.5 with breakout board v1.2
Copyright (c) 2019, 2020 Yuichi Takeuchi
'''

from pyControl.utility import *
import hardware_definition as hw # hw_GoNoGoTask_2v1.py

#-------------------------------------------------------------------------
# States and events.
#-------------------------------------------------------------------------
states = ['init_state',
          'intertrial_intrvl',
          'poke1_actv',
          'poke2_actv',
          'reward']

events = ['poke1_in',
          'poke1_out',
          'poke2_in',
          'poke2_out',
          'reward_on',
          'reward_off',
          'button_press', 	# USR button pressed
          'up',				# USR button released
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
v.intertrial_interval = 1 # intertrial interval in second
v.reward_taking_dulation = 1     # reward taking duration in second
v.reward_delivery_latency = 0		# latency for reward delivery in second
v.reward_delivery_duration = 100         # reward delivery duration in ms
v.Poke1LED = True
v.Poke2LED = True
v.Click = True

# Variables.
v.n_trials = 0                   # Number of trials recieved.
v.n_rewards = 0                  # Number of rewards obtained.

#-------------------------------------------------------------------------
# Non-state machine code.
#-------------------------------------------------------------------------

def print_current_state():
    # Print trial information.
    v.n_trials  +=1
    v.n_rewards +=1
    print('T#:{} R#:{}'.format(
           v.n_trials, v.n_rewards))

#-------------------------------------------------------------------------
# State machine code.
#-------------------------------------------------------------------------
# Run start and stop behaviours.
def run_start():
    pyb.LED(v.LED_n).on()
    hw.houselight1.on()
    hw.houselight2.on()
    hw.houselight3.on()
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
    elif event == 'button_press':
        goto('intertrial_intrvl')
    elif event == 'exit':
        pass

def intertrial_intrvl(event):
    # inter trial interval
    if event == 'entry':
        # print('intertial interval')
        timed_goto_state('poke1_actv', v.intertrial_interval*second)
    elif event == 'exit':
        pass

def poke1_actv(event):
    # wait for poke1
    if event == 'entry':
        if v.Poke1LED:
            hw.poke1.LED.on()
    elif event == 'poke1_in':
        if v.Click:
            hw.speaker.click()
        goto('poke2_actv')
    elif event == 'exit':
        hw.poke1.LED.off()

def poke2_actv(event):
    # wait for poke2
    if event == 'entry':
        if v.Poke2LED:
            hw.poke2.LED.on()
    elif event == 'poke2_in':
        if v.Click:
            hw.speaker.click()
        goto('reward')
    elif event == 'exit':
        hw.poke2.LED.off()

def reward(event):
    # Reward delivery from sol of poke
    if event == 'entry':
        set_timer('reward_on', v.reward_delivery_latency*second, output_event=True)
    elif event == 'reward_on':
        hw.poke2.SOL.on()
        set_timer('reward_off', v.reward_delivery_duration*ms, output_event=True)
        timed_goto_state('intertrial_intrvl', v.reward_taking_dulation*second)
    elif event == 'reward_off':
        hw.poke2.SOL.off()
    elif event == 'exit':
        hw.poke2.SOL.off()
        print_current_state()

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