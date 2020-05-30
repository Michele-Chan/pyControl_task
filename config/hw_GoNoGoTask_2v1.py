'''
Task control test with pyControl v1.5 with breakout board v1.2
hardware_definition
Copyright (c) 2019, 2020 Yuichi Takeuchi
'''

from devices import *

board = Breakout_1_2()

# Instantiate Devices.
# port 1
poke2 = Poke(port=board.port_1, rising_event = 'poke2_in'  , falling_event = 'poke2_out', debounce=50)

# port 2
#These houselights should be defined in each task file if more than one
houselight1 = Digital_output(pin='X4', inverted=False, pulse_enabled=False)
houselight2 = Digital_output(pin='X18', inverted=False, pulse_enabled=False)
houselight3 = Digital_output(pin='Y12', inverted=False, pulse_enabled=False)

# port 3
speaker = Audio_board(port=board.port_3)
speaker.set_volume = 63 #1-127

# port 4

# port 5
poke1 = Poke(port=board.port_5, rising_event = 'poke1_in'  , falling_event = 'poke1_out', debounce=50)

# port 6
punishment = Digital_output(pin=board.BNC_2, inverted=False, pulse_enabled=False)

# others
sync_output = Rsync(pin=board.BNC_1, event_name='rsync', mean_IPI=5000, pulse_dur=100)
pyboard_button = Digital_input(pin = 'X17', falling_event='button_press', pull='up')  # USR button on pyboard.

