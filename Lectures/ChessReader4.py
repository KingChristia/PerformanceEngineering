# 1. Imported Modules
# -------------------

import sys
import re

from ChessGame import *
from ChessDataBase import *

# 2. Main
# -------

dataBase = DataBase_New("Stockfish_15_64-bit.commented.[2600]")

game = Game_New("CCRL", "Ruy Lopez")
DataBase_AddGame(dataBase, game)

print(dataBase)
