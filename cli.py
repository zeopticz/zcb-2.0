# Command-line interface for ZCB.

if __name__ == '__main__':
    import os
    import sys

    # Function to clear terminal
    clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    # Import things
    from termcolor import colored
    from tkinter import filedialog as fd
    from tkinter import messagebox as mb
    clear() # Clear terminal

    ALLOWED_FILENAMES = ['echo', 'json']

    # Print some text
    print(colored('ZCB 2.0', 'white', 'on_green'))
    print(colored('Select a replay', 'yellow'))

    # Ask for macro file input
    macro_input = ''
    while macro_input == '': # Ask again and again until a file is selected
        macro_input = fd.askopenfilename()
        if macro_input == '':
            print(colored('No file selected!', 'red'))
        elif not macro_input.endswith(tuple(ALLOWED_FILENAMES)):
            print(colored(f'.{macro_input.split(".")[-1]} files are not supported.\n'
                  + f'Supported filenames: {"".join(ALLOWED_FILENAMES)}', 'red'))
            input()
            sys.exit()

    macro_filename = macro_input.split('/')[-1].split('.')[0]
    
    clear()
    print(colored('ZCB 2.0', 'white', 'on_green'))
    print(colored('Select a clickpack folder', 'yellow'))
    
    click_folder_input = ''
    while click_folder_input == '':
        click_folder_input = fd.askdirectory()
        if click_folder_input == '':
            print(colored('No folder selected!', 'red'))
    
    # Successfully retrieved filename, now parse it.
    clear()
    
    import parser
    if macro_input.endswith('echo'): # Parse echo file
        print(colored('Parsing...', 'white', 'on_green'))
        with open(macro_input, 'r') as f:
            try:
                p1_macro, p2_macro, replay_fps = parser.parse_echo(f.read())
            except Exception as e:
                print(colored(repr(e), 'red'))
                print(colored('Cannot parse file! This might happen when you are trying to import binary macros.', 'white', 'on_red'))
                input()
                sys.exit()
            f.close()
    elif macro_input.endswith('json'): # Parse TASbot file
        print(colored('Parsing...', 'white', 'on_green'))
        with open(macro_input, 'r') as f:
            try:
                p1_macro, p2_macro, replay_fps = parser.parse_tasbot(f.read())
            except Exception as e:
                print(colored(repr(e), 'red'))
                print(colored('Cannot parse file! Something is wrong with your replay, or it is not a TASbot replay.', 'white', 'on_red'))
                input()
                sys.exit()
            f.close()

    # TODO: add support for other file formats.

    # Successfully retrieved click pack folder, now parse it. (this also prints debug info)
    from discover_clicks import discover_clicks
    p1_clicks, p2_clicks, p1_releases, p2_releases, p1_softclicks, p2_softclicks, p1_softreleases, p2_softreleases = discover_clicks(click_folder_input)

    input('\nPress Enter to continue')

    clear()

    print(colored(f'File: "{macro_input}"', 'white', 'on_green'))
    print(colored(f'FPS: {round(replay_fps)}', 'white', 'on_red'))
    print(colored(f'Actions: {"{0:,}".format(len(p1_macro) + len(p2_macro))}', 'white', 'on_red'))

    # Softclick delay input.
    softclick_delay = ''
    while softclick_delay == '':
        softclick_delay = input('\nSoftclick delay (ms, press Enter for default value): ')
        if softclick_delay == '':
            softclick_delay = 'default'
        if not softclick_delay.isdigit():
            softclick_delay = 'default'
    
    # Do use sound pitch?
    use_sound_pitch = ''
    while use_sound_pitch == '':
        use_sound_pitch = mb.askyesno('Sound pitch', 'Do you want to pitch sound? This can add variation to clicks and make them more realistic.')
    
    from generate_clicks import generate_clicks

    #try:
    generate_clicks(

        # Sounds
        p1_clicks=p1_clicks,
        p2_clicks=p2_clicks,
        p1_releases=p1_releases,
        p2_releases=p2_releases,
        p1_softclicks=p1_softclicks,
        p2_softclicks=p2_softclicks,
        p1_softreleases=p1_softreleases,
        p2_softreleases=p2_softreleases,

        # Other stuff
        macro_filename=macro_filename,
        replay_fps=replay_fps,
        softclick_duration_option=softclick_delay,
        use_sound_pitch = use_sound_pitch,

        # Actual macro data
        p1_macro=p1_macro,
        p2_macro=p2_macro
    )
    #except Exception as e:
    #    print(colored(repr(e), 'red'))
    #    print(colored('ERROR: Something went wrong while generating clicks.', 'white', 'on_red'))
    #    input()
    #    sys.exit()
    
    print(colored(f'Done! You should see a file called "{macro_filename}" in the "output" folder.', 'white', 'on_green'))
    input()
