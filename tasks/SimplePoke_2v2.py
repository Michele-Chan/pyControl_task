'''
Task control test with pyControl v1.4 with breakout board v1.2
Copyright (c) 2019, 2020 Yuichi Takeuchi
'''

from pyControl.utility import *
import hardware_definition as hw  # hw_GoNoGoTask_2v1.py

# -------------------------------------------------------------------------
# States and events.
# -------------------------------------------------------------------------
states = ['init_state',
          'poke2_actv',
          'reward']

events = ['poke2_in',
          'poke2_out',
          'reward_on',
          'reward_off',
          'button_press', 	# USR button pressed
          'blinker_on',		# pyboard LED on
          'blinker_off', 	# pyboard LED off
          'session_timer',
          'rsync']

initial_state = 'init_state'

# -------------------------------------------------------------------------
# Variables.
# -------------------------------------------------------------------------
# Parameters.
v.LED_n = 4  # Number of LED to use.
v.session_duration = 1     # Session duration in hour
v.reward_state_dulation = 2     # reward deliver state duration in second
v.reward_delivery_duration = 200     # reward delivery duration in ms
v.PokeLED = True
v.Click = True

# Variables.
v.n_trials = 0                   # Number of trials recieved.
v.n_rewards = 0                  # Number of rewards obtained.


# -------------------------------------------------------------------------
# Non-state machine code.
# -------------------------------------------------------------------------
def print_current_state():
    # Print trial information.
    v.n_trials += 1
    v.n_rewards += 1
    print('T#:{} R#:{}'.format(
           v.n_trials, v.n_rewards))


# -------------------------------------------------------------------------
# State machine code.
# -------------------------------------------------------------------------
# Run start and stop behaviours.
def run_start():
    pyb.LED(v.LED_n).on()
    hw.houselight1.on()
    hw.houselight2.on()
    hw.houselight3.on()
    set_timer('blinker_off', 1*second)  # option: output_event=True
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
        goto('poke2_actv')


def poke2_actv(event):
    # wait for poke
    if event == 'entry':
        if v.PokeLED:
            hw.poke2.LED.on()
    elif event == 'exit':
        hw.poke2.LED.off()
    elif event == 'poke2_in':
        if v.Click:
            hw.speaker.click()
        goto('reward')


def reward(event):
    # Reward delivery from sol of poke
    if event == 'entry':
        set_timer('reward_on', 0*ms, output_event=True)
        hw.poke2.SOL.on()
        set_timer('reward_off', v.reward_delivery_duration*ms, output_event=True)
        timed_goto_state('poke2_actv', v.reward_state_dulation*second)
    elif event == 'exit':
        hw.poke2.SOL.off()
        print_current_state()
    elif event == 'reward_off':
        hw.poke2.SOL.off()


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
    elif event == 'session_timer':  # session timer for framework
        stop_framework()
