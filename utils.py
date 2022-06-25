import json
from pydub import AudioSegment
import random
from tqdm import tqdm
import sys
from os import walk, path, _exit, listdir, mkdir

class colors:
    reset = '\033[0m'
    fg = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }

    bg = {
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m'
    }

def cprint(text, color, bg=False):
    background = colors.bg[bg] if bg else ''
    print(colors.fg[color] + background + text + colors.reset)

class log:
    def printwarn(text):
        print(f'[{colors.fg["yellow"]}!{colors.reset}]{colors.fg["yellow"]} WARNING: {colors.reset}{text}{colors.reset}')
    def printerr(text):
        print(f'[{colors.fg["red"]}-{colors.reset}]{colors.fg["red"]} ERROR: {colors.reset}{text}{colors.reset}')
    def printinfo(text):
        print(f'[{colors.fg["blue"]}i{colors.reset}]{colors.fg["blue"]} INFO: {colors.reset}{text}{colors.reset}')
    def printsuccess(text):
        print(f'[{colors.fg["green"]}+{colors.reset}]{colors.fg["green"]} SUCCESS: {colors.reset}{text}{colors.reset}')

class parser:
    def parse_echo(replay_file):
        '''
        Parses .echo files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = json.loads(replay_file)
        replay_fps = int(round(replay['FPS']))
        replay_data = replay['Echo Replay']
        last_click_action = False
        last_p2_click_action = False

        p1_clicks = []
        p2_clicks = []

        for frame in replay_data: # Iterate through every frame of the macro.
            last_frame = frame['Frame']
            last_action = frame['Hold']
            is_p2 = frame["Player 2"]
            try:
                is_action = frame['Action']
            except Exception:
                is_action = True

            if not is_p2: # If the action is from player 1.
                if last_action and not last_click_action and is_action:
                    last_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p1_clicks.append([last_frame, 'click'])

                elif not last_action and last_click_action and is_action:
                    last_click_action = False
                    p1_clicks.append([last_frame, 'release'])
            else: # If the action is from player 2.
                if last_action and not last_p2_click_action and is_action:
                    last_p2_click_action = True
                    '''
                    list of lists:
                    [[frame, 'click'/'release'], ...]
                    '''
                    p2_clicks.append([last_frame, 'click'])

                elif not last_action and last_p2_click_action and is_action:
                    last_p2_click_action = False
                    p2_clicks.append([last_frame, 'release'])
                else:
                    pass
        
        return p1_clicks, p2_clicks, replay_fps # Return parsed macro.

    def parse_tasbot(replay_file):
        '''
        Parses .json (tasbot) files.
        Returns:
        p1_clicks, p2_clicks, replay_fps
        ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
        [frame, 'click'/'release']
        '''
        # Define basic info.
        replay = json.loads(replay_file)
        replay_fps = int(round(replay['fps']))
        replay_data = replay['macro']
        last_click_action = False
        last_p2_click_action = False

        p1_clicks = []
        p2_clicks = []

        for frame in replay_data: # Iterate through every frame of the macro.
            last_frame = frame['frame']
            
            player_1_frame = frame['player_1']
            player_2_frame = frame['player_2']

            last_p1_action = player_1_frame['click'] == 1
            last_p2_action = player_2_frame['click'] == 1

            if not last_click_action and last_p1_action:
                last_click_action = True
                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p1_clicks.append([last_frame, 'click'])
            elif not last_p1_action and last_click_action: # If the action is from player 1.
                last_click_action = False
                p1_clicks.append([last_frame, 'release'])

            if not last_p2_click_action and last_p2_action: # If the action is from player 2.
                last_p2_click_action = True

                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p2_clicks.append([last_frame, 'click'])
            elif not last_p2_action and last_p2_click_action:
                last_click_action = False
                p2_clicks.append([last_frame, 'release'])

        return p1_clicks, p2_clicks, replay_fps

def discover_clicks(folder: str):
    '''Processes a clickpack.
    '''

    p1_click_folders = list()
    p2_click_folders = list()

    
    player_dirs = listdir(folder)
    log.printinfo(f'Player directories: {player_dirs}')

    '''
    Now, for player_dir (player1, player2) we will have to process click folders
    (clicks, releases, softclicks, softreleases)
    '''
    for player_dir in player_dirs:
        log.printinfo(f'Observing Path: {path.join(folder, player_dir)}')
        log.printinfo(f'Current Player Directory: {player_dir}')

        for (dirnames, _, _) in walk(path.join(folder, player_dir)):
            log.printinfo(f'Current Directories: {dirnames}')

            if player_dir == 'player1':
                if not dirnames.endswith(player_dir):
                    p1_click_folders.append(dirnames) 

            elif player_dir == 'player2':
                if not dirnames.endswith(player_dir):
                    p2_click_folders.append(dirnames) 
    log.printsuccess(f'Finished discovering click folders! Now processing Media.')

    p1_clicks = list()
    p2_clicks = list()
    p1_releases = list()
    p2_releases = list()

    
    p1_softclicks = list()
    p2_softclicks = list()
    p1_softreleases = list()
    p2_softreleases = list()

    log.printinfo(f'Player 1 clicks finished!')
    for folder in p1_click_folders:
        log.printinfo(f'Current Directory: {folder}')
        for (_, _, filenames) in walk(folder):
            log.printinfo(f'This folder contains: {filenames}')
            current_click_type = folder.split('\\')[-1]

            log.printinfo(f'Current Folder Type: {current_click_type}')
            log.printinfo(f'Current Player: Player 1')
            
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): 
                    log.printinfo(f'Adding File: {file}')
                    full_paths.append(path.join(folder, file))
                    
                else:
                    log.printwarn(f'File is not a wav file! Skipping: {file}')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            
            for click_path in full_paths:
                try: 

                    
                    if current_click_type == 'clicks':
                        log.printsuccess(f'Finished Processing! ({click_path})')
                        p1_clicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'releases':
                        p1_releases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softclicks':
                        p1_softclicks.append(AudioSegment.from_wav(click_path))
                    if current_click_type == 'softreleases':
                        p1_softreleases.append(AudioSegment.from_wav(click_path))
                
                except Exception as e:
                    if click_path.endswith('.wav'): 

                        log.printerr(f'Failed to process "{click_path}", perhaps it\'s corrupted?')
                    else:
                        if not click_path.endswith('.txt'): 
                            log.printerr(f'Failed to process "{click_path}", perhaps it\'s not a .wav?')
    
    log.printinfo(f'Processing Player 2 clicks.')
    for folder in p1_click_folders:
        log.printinfo(f'Current Directory: {folder}')
        for (_, _, filenames) in walk(folder):
            log.printinfo(f'This folder contains: {filenames}')
            current_click_type = folder.split('\\')[-1]

            log.printinfo(f'Current Folder Type: {current_click_type}')
            log.printinfo(f'Current Player: Player 2')

            
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): 
                    log.printinfo(f'Adding File: {file}')
                    full_paths.append(path.join(folder, file))
                    
                else:
                    log.printwarn(f'File is not a wav file! Skipping: {file}')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            
            for click_path in full_paths:
                try: 

                    
                    if current_click_type == 'clicks':
                        log.printsuccess(f'Finished Processing! ({click_path})')
                        p2_clicks.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'releases':
                        p2_releases.append(AudioSegment.from_wav(click_path))
                    elif current_click_type == 'softclicks':
                        p2_softclicks.append(AudioSegment.from_wav(click_path))
                    if current_click_type == 'softreleases':
                        p2_softreleases.append(AudioSegment.from_wav(click_path))
                
                except Exception as e:
                    if click_path.endswith('.wav'): 

                        log.printerr(f'Failed to process "{click_path}", perhaps it\'s corrupted?')
                    else:
                        if not click_path.endswith('.txt'): 
                            log.printerr(f'Failed to process "{click_path}", perhaps it\'s not a .wav?')

    log.printinfo(f'Checking Info...\n')

    if p1_clicks == []:
        log.printerr(f'Player 1 has no clicks! Please follow the click format.')
        input('Press ENTER to continue...')
        _exit(0)
    if p2_clicks == []: 
        log.printwarn('Player 2 has no clicks! Using Player 1 clicks.')
        p2_clicks = p1_clicks

    if p1_releases == []:
        log.printwarn('Player 1 has no releases! Using Player 1 clicks.')
        p1_releases = p1_clicks
    if p2_releases == []:
        log.printwarn('Player 2 has no releases! Using Player 1 releases.')
        p2_releases = p1_releases

    if p1_softclicks == []:
        log.printwarn('Player 1 has no softclicks! Using Player 1 clicks.')
        p1_softclicks = p1_clicks
    if p2_softclicks == []:
        log.printwarn('Player 2 has no softclicks! Using Player 2 clicks.')
        p2_softclicks = p2_clicks
    
    if p1_softreleases == []:
        log.printwarn('Player 1 has no softreleases! Using Player 1 releases.')
        p1_softreleases = p1_releases
    if p2_softreleases == []:
        log.printwarn('Player 2 has no softreleases! Using Player 2 releases.')
        p2_softreleases = p2_releases
    
    log.printsuccess(f'Complete! Please check the log for any Errors, and press ENTER when ready.')

    '''Variables explanation
    
    p1_clicks = list()
    p2_clicks = list()
    p1_releases = list()
    p2_releases = list()

    p1_softclicks = list()
    p2_softclicks = list()
    p1_softreleases = list()
    p2_softreleases = list()

    Those can return an empty list if the folder does not exist:

    [0] - p1 clicks
    [1] - p2 clicks
    [2] - p1 releases
    [3] - p2 releases
    [4] - p1 softclicks
    [5] - p2 softclicks
    [6] - p1 softreleases
    [7] - p2 softreleases
    '''

    return (
        p1_clicks,
        p2_clicks,
        p1_releases,
        p2_releases,
        p1_softclicks,
        p2_softclicks,
        p1_softreleases,
        p2_softreleases,
    )

def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))

def generate_clicks(
                    p1_clicks, 
                    p2_clicks,
                    p1_releases,
                    p2_releases,
                    p1_softclicks,
                    p2_softclicks,
                    p1_softreleases,
                    p2_softreleases,

                    p1_macro,
                    p2_macro,
                    replay_fps,

                    softclick_duration_option,
                    macro_filename,
                    use_sound_pitch
                ):

    output_sound = AudioSegment.empty()
    output_sound = output_sound.set_frame_rate(44100) 
    
    try:
        audio_time = (p1_macro[-1][0] / replay_fps + p1_releases[0].duration_seconds if p1_releases[0].duration_seconds != 0 else 1 + 0.2) * 1000
    except IndexError: 
        audio_time = (p2_macro[-1][0] / replay_fps + p1_releases[0].duration_seconds if p1_releases[0].duration_seconds != 0 else 1 + 0.2) * 1000
    
    output_sound += AudioSegment.silent(audio_time)
    
    last_action_time = 0

    both_players_macro = [p1_macro, p2_macro] 

    pbar = tqdm(total=len(p1_macro) + len(p2_macro), colour='green', ascii=True, desc='Progress')

    current_player = 0

    for macro in both_players_macro:
        current_player += 1 

        if current_player == 1:
            softclicks = p1_softclicks
            softreleases = p1_softreleases
            clicks = p1_clicks
            releases = p1_releases
        
        else:
            softclicks = p2_softclicks
            softreleases = p2_softreleases
            clicks = p2_clicks
            releases = p2_releases
        
        for action in macro:

            if softclick_duration_option == 'default':
                
                softclick_duration = 120 + random.randint(0, 10)
            else: 
                softclick_duration = softclick_duration_option

            
            if (action[0] / replay_fps * 1000 - last_action_time < softclick_duration): 
                

                
                if action[1] == 'click':
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(softclicks)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(softclicks),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                else: 

                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(softreleases)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(softreleases),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
            
            else: 
                if action[1] == "click":
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(clicks)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(clicks),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                
                elif action[1] == "release":
                    if use_sound_pitch:
                        
                        pitched_sound = random.choice(releases)
                        octaves = random.uniform(-0.1, 0.1) 
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 
                    else:
                        
                        output_sound = output_sound.overlay(
                            seg=random.choice(releases),
                            position=action[0] / replay_fps * 1000, 
                        )
                        pbar.update(1) 

                last_action_time = action[0] / replay_fps * 1000
    
    pbar.close()

    if not path.isdir("output"):
        mkdir("output")
    export_path = path.join(get_script_path(), 'output', macro_filename + '.wav')

    print('\nExporting...')
    output_sound.export(export_path, format="wav")