# Data base of chess games

import ChessGame

def DataBase_New(name):
    return [name, []]

def DataBase_GetName(dataBase):
    return dataBase[0]

def DataBase_SetName(dataBase, name):
    dataBase[0] = name

def DataBase_GetGames(dataBase):
    return dataBase[1]

def DataBase_AddGame(dataBase, game):
    games = DataBase_GetGames(dataBase)
    games.append(game)
