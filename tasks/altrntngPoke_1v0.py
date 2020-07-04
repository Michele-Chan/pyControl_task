'''
Alternative poke task

Hardware definition file: hw_GoNoGoTask_2v1.py
Task control test with pyControl v1.5 with breakout board v1.2
Copyright (c) 2020 Yuichi Takeuchi
'''

from pyControl.utility import *
import hardware_definition as hw  # hw_GoNoGoTask_2v1.py

# -------------------------------------------------------------------------
# States and events.
# -------------------------------------------------------------------------
states = ['init_state',
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
          'blinker_on',		# pyboard LED on
          'blinker_off', 	# pyboard LED off
          'session_timer',
          'rsync']

initial_state = 'init_state'


# -------------------------------------------------------------------------
# Variables.
# -------------------------------------------------------------------------
# Parameters
v.LED_n = 4  # Number of LED to use.
v.session_duration = 1     # Session duration in hour
v.reward_state_dulation = 2     # reward deliver state duration in second
v.reward_delivery_duration = 200     # reward delivery duration in ms
v.PokeLED = True
v.Click = True

# Flags
v.poke1_flag = True

# Cummurative variables
v.n_trial = 0                   # Number of trials initiated
v.n_reward = 0                  # Number of rewards delivered


# -------------------------------------------------------------------------
# Non-state machine code.
# -------------------------------------------------------------------------
def print_current_state():
    # Print trial information.
    v.n_trial += 1
    v.n_reward += 1
    print('T#:{} R#:{}'.format(v.n_trial, v.n_reward))


def flip_flag():
    v.poke1_flag = not(v.poke1_flag)


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
        if v.poke1_flag:
            goto('poke1_actv')
        else:
            goto('poke2_actv')


def poke1_actv(event):
    # wait for poke
    if event == 'entry':
        if v.PokeLED:
            hw.poke1.LED.on()
    elif event == 'exit':
        hw.poke1.LED.off()
    elif event == 'poke1_in':
        if v.Click:
            hw.speaker.click()
        goto('reward')


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
        if v.poke1_flag:
            hw.poke1.SOL.on()
            timed_goto_state('poke2_actv', v.reward_state_dulation*second)
        else:
            hw.poke2.SOL.on()
            timed_goto_state('poke1_actv', v.reward_state_dulation*second)
        set_timer('reward_off', v.reward_delivery_duration*ms, output_event=True)
        flip_flag()
    elif event == 'reward_off':
        hw.poke1.SOL.off()
        hw.poke2.SOL.off()
    elif event == 'exit':
        hw.poke1.SOL.off()
        hw.poke2.SOL.off()
        print_current_state()


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
