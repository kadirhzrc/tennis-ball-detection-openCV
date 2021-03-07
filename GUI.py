import PySimpleGUI as sg
import subprocess
import sys

# Add some color
# to the window
sg.theme('SandyBeach')

# Very basic window.
# Return values using
# automatic-numbered keys
layout = [
    [sg.Text('Leave empty for webcam as source or enter the name of the .mp4 file.')],
    [sg.Text('.mp4 name', size=(15, 1)), sg.InputText()],
    [sg.Text('Buffer size (optional)', size=(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Tennis Ball Tracker', layout)
event, values = window.read()
window.close()

# The input data looks like a simple list
# when automatic numbered
print(event, values[0], values[1])

if event == 'Submit':
    if not values[0]:
        if values[1]:
            subprocess.call('main.py --buffer ' + values[1], shell=True)
        else:
            subprocess.call('main.py', shell=True)
    else:
        if values[1]:
            subprocess.call('main.py --video ' + values[0] + ' --buffer ' + values[1], shell=True)
        else:
            subprocess.call('main.py --video ' + values[0], shell=True)
else:
    sys.exit()