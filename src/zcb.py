import sys
sys.dont_write_bytecode = True

from utils import *
import os
import traceback

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

from tkinter import filedialog as fd
from tkinter import messagebox as mb

clear()

ALLOWED_FILENAMES = ['echo', 'json']

print('''
███████╗ ██████╗██████╗ 
╚══███╔╝██╔════╝██╔══██╗
  ███╔╝ ██║     ██████╔╝
 ███╔╝  ██║     ██╔══██╗
███████╗╚██████╗██████╔╝ v2.0
╚══════╝ ╚═════╝╚═════╝ 
    Zeo's Click Bot
'''.replace('█', colors.fg['magenta']+'█'+colors.reset))
log.printinfo('Select a replay!')

macro_input = ''
while macro_input == '':
    macro_input = fd.askopenfilename()
    if macro_input == '':
        log.printerr('No File Selected!')
    elif not macro_input.endswith(tuple(ALLOWED_FILENAMES)):
        log.printerr(f'That file type is not supported! \
                Supported File Types: {"".join(ALLOWED_FILENAMES)}')
        input()
        sys.exit()

macro_filename = macro_input.split('/')[-1].split('.')[0]

clear()
log.printinfo('Select a clickpack!')

click_folder_input = ''
while click_folder_input == '':
    click_folder_input = fd.askdirectory()
    if click_folder_input == '':
        log.printerr('No Folder Selected!')

clear()

if macro_input.endswith('echo'):
    log.printinfo(f'Parsing File: {macro_input}')
    with open(macro_input, 'r') as f:
        try:
            p1_macro, p2_macro, replay_fps = parser.parse_echo(f.read())
        except Exception as e:
            log.printerr(f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
            input()
            sys.exit()
        f.close()
elif macro_input.endswith('json'):
    log.printinfo(f'Parsing File: {macro_input}')
    with open(macro_input, 'r') as f:
        try:
            p1_macro, p2_macro, replay_fps = parser.parse_tasbot(f.read())
        except Exception as e:
            log.printerr(f'An Error occured while parsing replay!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
            input()
            sys.exit()
        f.close()

p1_clicks, p2_clicks, p1_releases, p2_releases, p1_softclicks, p2_softclicks, p1_softreleases, p2_softreleases = discover_clicks(click_folder_input)

input('\nPress ENTER to continue...')

clear()

log.printinfo(f'File: "{macro_input}"')
log.printinfo(f'FPS: {round(replay_fps)}')
log.printinfo(f'Actions: {"{0:,}".format(len(p1_macro) + len(p2_macro))}')

softclick_delay = ''
while softclick_delay == '':
    softclick_delay = input('\nSoftclick Delay (In MS, Leave blank for default value) > ')
    if softclick_delay == '':
        softclick_delay = 'default'
    if not softclick_delay.isdigit() and not softclick_delay == 'default':
        log.printerr('That is not a number!')
        softclick_delay = ''
    elif softclick_delay != 'default':
        softclick_delay = int(softclick_delay)

use_sound_pitch = ''
while use_sound_pitch == '':
    use_sound_pitch = mb.askyesno('ZCB - Sound Pitch', 'Do you want to pitch sound?\nThis adds more variability to clicks, which can make it sound more real.\nThis has minimal impact on rendering speed.')

try:
    generate_clicks(

        p1_clicks=p1_clicks,
        p2_clicks=p2_clicks,
        p1_releases=p1_releases,
        p2_releases=p2_releases,
        p1_softclicks=p1_softclicks,
        p2_softclicks=p2_softclicks,
        p1_softreleases=p1_softreleases,
        p2_softreleases=p2_softreleases,

        macro_filename=macro_filename,
        replay_fps=replay_fps,
        softclick_duration_option=softclick_delay,
        use_sound_pitch = use_sound_pitch,

    p1_macro=p1_macro,
    p2_macro=p2_macro
)
except Exception:
    log.printerr(f'An Error occured while generating clicks!\nIf the issue persists, please contact support!\nError: {traceback.format_exc()}')
    input()
    sys.exit()

log.printsuccess(f'Clicks Created. You will find a file named "{macro_filename}" in the "output" folder!')
input()
