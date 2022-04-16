'''Longass function to process a clickpack.
how is this 273 lines
'''

from pydub import AudioSegment
from os import walk, path
from sys import exit as sysexit
from termcolor import cprint # Prettier color prints

def discover_clicks(folder: str):
    '''Processes a clickpack.
    '''

    # print('Not using ffmpeg for pydub - defaulting to avconv')
    # AudioSegment.converter = 'avconv'

    # Click folders are lists of: clicks, releases, softclicks, softreleases.
    p1_click_folders = list()
    p2_click_folders = list()

    # Here, this outputs player1 and player2 folders (list)
    for (_, dirnames, _) in walk(folder):
        player_dirs = dirnames
        break
    cprint(f'INFO: Player directories: {player_dirs}', 'cyan')

    '''
    Now, for player_dir (player1, player2) we will have to process click folders
    (clicks, releases, softclicks, softreleases)
    '''
    for player_dir in player_dirs:
        cprint(f'INFO: Observing path: {path.join(folder, player_dir)}', 'cyan')
        cprint(f'INFO: Current player directory: {player_dir}', 'cyan')

        # Dirnames are [clicks, releases, softclicks, softreleases] for both players.
        for (dirnames, _, _) in walk(path.join(folder, player_dir)):
            cprint(f'INFO: Current dirnames: {dirnames}', 'cyan')

            # If player directory we're currently in is player1, we will have to append the folder
            # to the player 1 click folders variable.
            # if not dirnames.endswith(player_dir) checks if it isn't the same folder.
            if player_dir == 'player1':
                if not dirnames.endswith(player_dir):
                    p1_click_folders.append(dirnames) # Append to click folder list

            # Else, if player directory we're currently in is player2, we will have to append the folder
            # to the player 1 click folders variable.
            # if not dirnames.endswith(player_dir) checks if it isn't the same folder.
            elif player_dir == 'player2':
                if not dirnames.endswith(player_dir):
                    p2_click_folders.append(dirnames) # Append to click folder list
    
    # Now, we have all of the click folders needed. All we need to do now is to
    # make each file a Pydub's AudioSegment.
    cprint('INFO: Finished discovering click folders. Now processing files.', 'cyan')

    # Those will contain AudioSegment's in future.

    # Default clicks + releases.
    p1_clicks = list()
    p2_clicks = list()
    p1_releases = list()
    p2_releases = list()

    # Softclicks + softreleases
    p1_softclicks = list()
    p2_softclicks = list()
    p1_softreleases = list()
    p2_softreleases = list()

    # Now, for each folder in click folders, get filenames and append to the lists
    # we created earlier.

    # THIS IS FOR PLAYER 1.
    cprint('INFO: Processing player1 clicks.', 'white', 'on_green')
    for folder in p1_click_folders:
        cprint(f'INFO: Currently in folder: {folder}', 'cyan')
        for (_, _, filenames) in walk(folder):
            cprint(f'INFO: This folder contains: {filenames}', 'cyan')
            current_click_type = folder.split('\\')[-1]

            cprint(f'INFO: Current click folder type: {current_click_type}', 'cyan') # (softclicks, releases, clicks, ...)
            cprint('INFO: Current player: player1', 'cyan') # We know this because we only browse p1_click_folders.

            # Filenames contain ['1.wav', '2.wav', ...]
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): # Only support .wav files
                    cprint(f'INFO: Adding {file} to the full path list.', 'cyan')
                    full_paths.append(path.join(folder, file))
                    # List of full file paths to clicks.
                else:
                    cprint(f'WARN: "{file}" is not a ".wav" file! Skipping.', 'yellow')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            # For each click in this folder,
            for click_path in full_paths:
                try: # This could fail if something is wrong with the file.

                    # Append AudioSegment to list depending on the current click type.
                    if current_click_type == 'clicks':
                        p1_clicks.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    elif current_click_type == 'releases':
                        p1_releases.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    elif current_click_type == 'softclicks':
                        p1_softclicks.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    if current_click_type == 'softreleases':
                        p1_softreleases.append(AudioSegment.from_wav(click_path))
                        cprint(f'INFO: Processed "{click_path}"', 'cyan')
                
                except Exception as e:
                    cprint(repr(e), 'red')
                    if click_path.endswith('.wav'): # Check if the path actually ends with .wav.
                                                    # The audio file could be corrupted.
                        cprint(f'ERROR: cannot process file "{click_path}". Is the audio file corrupted?', 'white', 'on_red')
                    else:
                        if not click_path.endswith('.txt'): # Ignore text files
                            # The file is not a .wav file, throw an error.
                            cprint(f'ERROR: cannot process file "{click_path}". It is not a .wav file.', 'white', 'on_red')
    

    # THIS IS FOR PLAYER 2.
    cprint('INFO: Processing player2 clicks.', 'white', 'on_green')
    for folder in p2_click_folders:
        cprint(f'INFO: Currently in folder: {folder}', 'cyan')
        for (_, _, filenames) in walk(folder):
            cprint(f'INFO: This folder contains: {filenames}', 'cyan')
            current_click_type = folder.split('\\')[-1]

            cprint(f'INFO: Current click folder type: {current_click_type}', 'cyan') # (softclicks, releases, clicks, ...)
            cprint('INFO: Current player: player2', 'cyan') # We know this because we only browse p2_click_folders.

            # Filenames contain ['1.wav', '2.wav', ...]
            full_paths = list()
            for file in filenames:
                if file.endswith('.wav'): # Only support .wav files
                    cprint(f'INFO: Adding {file} to the full path list.', 'cyan')
                    full_paths.append(path.join(folder, file))
                    # List of full file paths to clicks.
                else:
                    cprint(f'WARN: "{file}" is not a ".wav" file! Skipping.', 'yellow')

            '''
            This checks if the current click type is clicks, releases, softclicks, ... and
            adds them to the lists we created earlier.
            '''
            # For each click in this folder,
            for click_path in full_paths:
                try: # This could fail if something is wrong with the file.

                    # Append AudioSegment to list depending on the current click type.
                    if current_click_type == 'clicks':
                        p2_clicks.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    elif current_click_type == 'releases':
                        p2_releases.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    elif current_click_type == 'softclicks':
                        p2_softclicks.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                    if current_click_type == 'softreleases':
                        p2_softreleases.append(AudioSegment.from_wav(click_path))
                        cprint(f'Processed "{click_path}"', 'cyan')
                
                except Exception as e:
                    cprint(repr(e), 'red')
                    cprint(f'ERROR: cannot process file "{click_path}". Is the audio file corrupted?', 'white', 'on_red')
    
    # Warnings if some files are not found.
    # The print() is needed for the line above the colored print to not be red.
    cprint('INFO: Checking if everything is OK...\n', 'cyan')

    # Clicks
    if p1_clicks == []: # Player 1
        cprint('ERROR: There are no clicks for player 1! Please follow the click format.', 'white', 'on_red')
        input('Press Enter to exit...')
        sysexit()
    if p2_clicks == []: # Player 2
        cprint("WARN: Player 2 clicks are empty! Will use player1 clicks.", 'yellow')
        p2_clicks = p1_clicks

    # Releases
    if p1_releases == []: # Player 1
        cprint("WARN: Can't find releases for player 1: will use clicks instead.", 'yellow')
        p1_releases = p1_clicks
    if p2_releases == []: # Player 2
        cprint("WARN: Can't find releases for player 2. Will use player 1 releases.", 'yellow')
        p2_releases = p1_releases

    # Softclicks
    if p1_softclicks == []: # Player 1
        cprint("WARN: Can't find player 1 softclicks. Will use default player 1 clicks instead.", 'yellow')
        p1_softclicks = p1_clicks
    if p2_softclicks == []: # Player 2
        cprint("WARN: Can't find player 2 softclicks. Will use default player 2 clicks instead.", 'yellow')
        p2_softclicks = p2_clicks
    
    # Softreleases
    if p1_softreleases == []: # Player 1
        cprint("WARN: Can't find player 1 softreleases. Will use default player 1 releases instead.", 'yellow')
        p1_softreleases = p1_releases
    if p2_softreleases == []: # Player 2
        cprint("WARN: Can't find player 2 softreleases. Will use default player 2 releases instead.", 'yellow')
        p2_softreleases = p2_releases
    
    
    cprint('INFO: All finished! Check the console for warnings and debug info before complaining about errors.', 'white', 'on_green')

    '''Variables explanation
    # Default clicks + releases.
    p1_clicks = list()
    p2_clicks = list()
    p1_releases = list()
    p2_releases = list()

    # Softclicks + softreleases
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

if __name__ == '__main__':
    # This will only run if you run this file directly.
    # Used for debugging
    p1_clicks, p2_clicks, p1_releases, p2_releases, p1_softclicks, p2_softclicks, p1_softreleases, p2_softreleases = discover_clicks(folder='C:/Users/user/Desktop/Projects/ZCB 2.0/clicks-example'.replace('/', '\\'))

    # Outputs Pydub AudioSegment object lists.
    print('p1 clicks', p1_clicks)
    print('p2 clicks', p2_clicks)
    print('p1 releases', p1_releases)
    print('p2 releases', p2_releases)
    print('p1 softclicks', p1_softclicks)
    print('p2 softclicks', p2_softclicks)
    print('p1 softreleases', p1_softreleases)
    print('p2 softreleases', p2_softreleases)