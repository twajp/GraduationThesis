import os
import sys
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from telemetrix import telemetrix
import keyboard

otTime = 2/3*(3-1)
logFilePath = logFilePath = os.path.expanduser('~/Desktop') + '/TSLog_' + datetime.now().strftime('%Y%m%d_%H%M') + '.csv'

LEFT_PIN = 12
RIGHT_PIN = 13
PINS = (LEFT_PIN, RIGHT_PIN)

CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

mode = 1
run_flag = False
signal_info = ''
previous_data = []
latest_data = []
# previous_signal_data = []


def the_callback(data):
    global previous_data
    global latest_data
    global run_flag

    latest_data = data
    run_flag = True
    previous_data = data


def digital_in_pullup(my_board, PINS):
    for pin in PINS:
        my_board.set_pin_mode_digital_input_pullup(pin, the_callback)

    print('Enter Control-C to quit.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)


def signal_ckecker():
    while True:
        global run_flag
        global mode
        global latest_data
        global signal_info
        global logFilePath

        if latest_data != []:
            latest_log_time = datetime.fromtimestamp(latest_data[CB_TIME])

        while run_flag:
            if previous_data != [] and datetime.now() > latest_log_time+timedelta(seconds=0.1):
                message = f'Time Stamp,{latest_log_time.isoformat()},Pin,{latest_data[CB_PIN]},Mode,{mode},'
                if latest_data[CB_PIN] == 13 and latest_data[CB_VALUE] == 0:
                    message += 'left on'
                    signal_info = 'left on'
                elif latest_data[CB_PIN] == 13 and latest_data[CB_VALUE] == 1:
                    message += 'left off'
                    signal_info = 'left off'
                elif latest_data[CB_PIN] == 12 and latest_data[CB_VALUE] == 0:
                    message += 'right on'
                    signal_info = 'right on'
                elif latest_data[CB_PIN] == 12 and latest_data[CB_VALUE] == 1:
                    message += 'right off'
                    signal_info = 'right off'

                print(message)
                with open(logFilePath, mode='a') as f:
                    f.write(message+'\n')
                run_flag = False
        time.sleep(0.01)


def signal_executor():
    global signal_info
    global otTime
    global mode
    while True:
        if signal_info == 'left on':
            keyboard.press('a')
            if mode != 1:
                time.sleep(otTime)
                while signal_info == 'left on':
                    time.sleep(1)
                keyboard.release('a')
                signal_info = ''
        elif signal_info == 'left off':
            keyboard.release('a')
            signal_info = ''
        elif signal_info == 'right on':
            keyboard.press('d')
            if mode != 1:
                time.sleep(otTime)
                while signal_info == 'right on':
                    time.sleep(1)
                keyboard.release('d')
                signal_info = ''
        elif signal_info == 'right off':
            keyboard.release('d')
            signal_info = ''
        time.sleep(0.01)


def mode_changer():
    global mode
    global otTime
    while True:
        if keyboard.read_key() == "1":
            if mode != 1:
                mode = 1
                print("Current Mode: 1")
        elif keyboard.is_pressed("3"):
            if mode != 3:
                mode = 3
                otTime = 2/3*(3-1)
                print("Current Mode: 3")
        elif keyboard.is_pressed("5"):
            if mode != 5:
                mode = 5
                otTime = 2/3*(5-1)
                print("Current Mode: 5")


board = telemetrix.Telemetrix()

try:
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(digital_in_pullup, board, PINS)
        executor.submit(signal_ckecker)
        executor.submit(signal_executor)
        executor.submit(mode_changer)
    # digital_in_pullup(board, PINS)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
