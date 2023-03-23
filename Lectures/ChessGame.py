# Chess Games

def Game_New(event, opening):
    return [event, opening]

def Game_GetEvent(game):
    return game[0]

def Game_SetEvent(game, event):
    game[0] = event

def Game_GetOpening(game):
    return game[1]

def Game_SetOpening(game, opening):
    game[1] = opening
