# The ZCB
from pydub import AudioSegment # All audio operations
import random # Used for "default" option in softclicks.
from os import path, mkdir
import sys
from tqdm import tqdm

def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))

def generate_clicks(
                    p1_clicks, # Click sounds lists
                    p2_clicks,
                    p1_releases,
                    p2_releases,
                    p1_softclicks,
                    p2_softclicks,
                    p1_softreleases,
                    p2_softreleases,

                    # Parsed macro data
                    p1_macro,
                    p2_macro,
                    replay_fps,

                    # Other options
                    softclick_duration_option,
                    macro_filename,
                    use_sound_pitch
                ):

    # Start with generating an empty AudioSegment.
    output_sound = AudioSegment.empty()
    output_sound = output_sound.set_frame_rate(44100) # Pydub won't set this automatically (cuz it's empty duh)

    # Audio time = (the last frame of macro / fps of replay (to get seconds) + release duration time + 0.2 of silence) * 1000 (to get ms)
    audio_time = (p1_macro[-1][0] / replay_fps + p1_releases[0].duration_seconds + 0.2) * 1000
    
    # Add (macro second length) of silence to our empty AudioSegment
    output_sound += AudioSegment.silent(audio_time)
    
    # The last frame where we added a click. Used for softclicks.
    last_action_time = 0

    # Macro for both players
    both_players_macro = [p1_macro, p2_macro] # ah yes, you can't do that. PLEASE FIX SO IT OUTPUTS LIST IN A LIST AND NOT LIST OF LISTS

    # Create tqdm progressbar
    pbar = tqdm(total=len(p1_macro) + len(p2_macro), colour='green', ascii=True, desc='Progress')

    # Current player
    current_player = 0

    # First up we will process player 1 clicks and macro.
    # Then, we will process player 2 clicks and macro.
    for macro in both_players_macro:

        # Switch thru player 1 and player 2 clicks
        current_player += 1 # Switch to next player

        # If the current player is 1, the clicks should be from player 1.
        if current_player == 1:
            softclicks = p1_softclicks
            softreleases = p1_softreleases
            clicks = p1_clicks
            releases = p1_releases
        # If the current player is 2, the clicks should be from player 2.
        else:
            softclicks = p2_softclicks
            softreleases = p2_softreleases
            clicks = p2_clicks
            releases = p2_releases
        
        for action in macro:

            # Get softclick duration to check if use softclicks later.
            if softclick_duration_option == 'default':
                # We create an another variable because we will be constantly changing it.
                softclick_duration = 120 + random.randint(0, 10)
            else: # If we got custom softclick duration
                softclick_duration = softclick_duration_option

            # print('Softclick duration:', softclick_duration)
            if (action[0] / replay_fps * 1000 - last_action_time < softclick_duration): # If it's the time to insert a softclick/softrelease
                # All code here will only run if we need to make a softclick/softrelease.

                # If the action is to click:
                if action[1] == 'click':

                    if use_sound_pitch:
                        # Create a pitched sound.
                        pitched_sound = random.choice(softclicks)
                        octaves = random.uniform(-0.1, 0.1) # Randomize pitch.
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        # Add the pitched sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                    else:
                        # Add the regular sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=random.choice(softclicks),
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                else: # Else if we need to place a softrelease (elif action[1] == 'release')

                    if use_sound_pitch:
                        # Create a pitched sound.
                        pitched_sound = random.choice(softreleases)
                        octaves = random.uniform(-0.1, 0.1) # Randomize pitch.
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        # Add the pitched sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                    else:
                        # Add the regular sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=random.choice(softreleases),
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
            
            else: # If it's a regular click and not a softclick

                if action[1] == "click":

                    if use_sound_pitch:
                        # Create a pitched sound.
                        pitched_sound = random.choice(clicks)
                        octaves = random.uniform(-0.1, 0.1) # Randomize pitch.
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        # Add the pitched sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                    else:
                        # Add the regular sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=random.choice(clicks),
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                
                elif action[1] == "release":

                    if use_sound_pitch:
                        # Create a pitched sound.
                        pitched_sound = random.choice(releases)
                        octaves = random.uniform(-0.1, 0.1) # Randomize pitch.
                        new_sample_rate = int(pitched_sound.frame_rate * (1.5 ** octaves))
                        pitched_sound = pitched_sound._spawn(pitched_sound.raw_data, overrides={'frame_rate': new_sample_rate})
                        pitched_sound = pitched_sound.set_frame_rate(44100)

                        # Add the pitched sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=pitched_sound,
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                    else:
                        # Add the regular sound at the right position.
                        output_sound = output_sound.overlay(
                            seg=random.choice(releases),
                            position=action[0] / replay_fps * 1000, # Pydub uses milliseconds.
                        )
                        pbar.update(1) # Update progressbar
                
                # Set the last action time of when we did a click.
                # Used for softclicks/softreleases.
                last_action_time = action[0] / replay_fps * 1000
    
    pbar.close() # Close progressbar, since we're finished

    # We processed everything, ready to export OwO
    if not path.isdir("output"):
        mkdir("output")
    export_path = path.join(get_script_path(), 'output', macro_filename + '.wav')

    print('\nExporting...')
    output_sound.export(export_path, format="wav")
