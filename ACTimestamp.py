import os
from time import sleep
from datetime import datetime, timedelta
import keyboard

r_count = 0
l_count = 0
x_count = 0
c_count = 0

previous_button_state = False
button_state = False
last_log = datetime.now()-timedelta(days=3)

logFilePath = os.path.expanduser('~/Desktop') + '/ACTimestamp_' + datetime.now().strftime('%Y%m%d_%H%M') + '.csv'

while True:
    if keyboard.is_pressed('right arrow') == True:
        button_state = 'r'
    elif keyboard.is_pressed('left arrow') == True:
        button_state = 'l'
    elif keyboard.is_pressed('x') == True:
        button_state = 'x'
    elif keyboard.is_pressed('c') == True:
        button_state = 'c'
    else:
        button_state = False

    if button_state != previous_button_state:
        if button_state != False:
            if button_state == 'r':
                r_count += 1
            elif button_state == 'l':
                l_count += 1
            elif button_state == 'x':
                x_count += 1
            elif button_state == 'c':
                c_count += 1
            message = f'{datetime.now().isoformat()},{button_state}, R:{r_count} L:{l_count} X:{x_count} c:{c_count}'
            last_log = datetime.now()
            print(message)
            with open(logFilePath, mode='a') as f:
                f.write(message+'\n')

    previous_button_state = button_state
    sleep(0.01)
