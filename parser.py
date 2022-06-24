import json

def parse_echo(replay_file):
    '''
    Parses .echo files.
    Returns:
    p1_clicks, p2_clicks, replay_fps
    ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
    [frame, 'click'/'release']
    '''

    replay = json.loads(replay_file)
    replay_fps = int(round(replay['FPS']))
    replay_data = replay['Echo Replay']
    last_click_action = False
    last_p2_click_action = False

    # Initialize lists to add actions to.
    p1_clicks = []
    p2_clicks = []

    for frame in replay_data:
        last_frame = frame['Frame']
        last_action = frame['Hold']
        is_p2 = frame["Player 2"]
        try:
            is_action = frame['Action']
        except: # if the macro is converted
            is_action = True


        # Player 1 & Player 2
        if not is_p2:
            # Player 1
            if last_action == True and last_click_action == False and is_action: # if clicked
                last_click_action = True

                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p1_clicks.append([last_frame, 'click'])

            elif last_action == False and last_click_action == True and is_action: # if released
                last_click_action = False
                p1_clicks.append([last_frame, 'release'])
        else:
            # Player 2
            if last_action == True and last_p2_click_action == False and is_action: # if clicked
                last_p2_click_action = True

                '''
                list of lists:
                [[frame, 'click'/'release'], ...]
                '''
                p2_clicks.append([last_frame, 'click'])

            elif last_action == False and last_p2_click_action == True and is_action: # if released
                last_p2_click_action = False
                p2_clicks.append([last_frame, 'release'])
            else:
                pass
    
    return p1_clicks, p2_clicks, replay_fps

def parse_tasbot(replay_file):
    '''
    Parses .json (tasbot) files.
    Returns:
    p1_clicks, p2_clicks, replay_fps
    ~~~~~~~~~  ~~~~~~~~~  ~~~~~~~~~~
    [frame, 'click'/'release']
    '''
    
    replay = json.loads(replay_file)
    replay_fps = round(int(replay['fps']))
    replay_data = replay['macro']
    last_click_action = False
    last_p2_click_action = False

    # Initialize lists to add actions to.
    p1_clicks = []
    p2_clicks = []

    for frame in replay_data:
        last_frame = frame['frame']
        
        player_1_frame = frame['player_1']
        player_2_frame = frame['player_2']

        last_p1_action = player_1_frame['click'] == 1 # True/False. 1 = is clicked, 2 = is not clicked.
        last_p2_action = player_2_frame['click'] == 1 # True/False. 1 = is clicked, 2 = is not clicked.


        # Player 1
        if last_click_action == False and last_p1_action: # if clicked
            last_click_action = True

            '''
            list of lists:
            [[frame, 'click'/'release'], ...]
            '''
            p1_clicks.append([last_frame, 'click'])
        elif last_p1_action == False and last_click_action == True: # if released
            last_click_action = False
            p1_clicks.append([last_frame, 'release'])

        # Player 2
        if last_p2_click_action == False and last_p2_action: # if clicked
            last_p2_click_action = True

            '''
            list of lists:
            [[frame, 'click'/'release'], ...]
            '''
            p2_clicks.append([last_frame, 'click'])
        elif last_p2_action == False and last_p2_click_action == True: # if released
            last_click_action = False
            p2_clicks.append([last_frame, 'release'])

    return p1_clicks, p2_clicks, replay_fps
