import PySimpleGUI as sg

layout = [[sg.Radio('pi', 'num', default=True) ,
           sg.Radio('42', 'num')],
          [sg.Button('Read')]]

window = sg.Window('Radio Button Example', layout)

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Cancel'):
        break
    print(event, values)

window.close()