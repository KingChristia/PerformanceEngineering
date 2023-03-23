import Move
import re


class ChessGame():

    def __init__(self, metadata, moves):
        self.metadata = metadata
        self.moves = moves
        self.winner = None

    def getMoves(self):
        return self.moves

    def numberOfMoves(self) -> int:
        return len(self.getMoves())

    def addMove(self, move1, move2):
        self.getMoves().append(Move.Move(move1, move2))

    def getMetadata(self):
        return self.metadata

    def getOpening(self):
        return self.getMetadata().get('Opening')

    def setMetadata(self, metadata):
        self.metadata = metadata

    def getEvent(self):
        return self.getMetadata()['Event']

    def getWinner(self):
        result = self.getMetadata().get('Result')
        if result == '1-0':
            return self.getMetadata().get('White')
        elif result == '0-1':
            return self.getMetadata().get('Black')
        else:
            return 'Draw'

    def getWin(self):
        return self.getMetadata().get('Result')

    def getWinningColor(self):
        result = self.getMetadata().get('Result')
        if result == '1-0':
            return 'White'
        elif result == '0-1':
            return 'Black'
        else:
            return 'Draw'

    # Task 3
    def exportToText(self, file):
        with open(file, 'w') as f:
            f.write('[Event "' + self.getMetadata().get('Event') + '"]\n')
            f.write('[Site "' + self.getMetadata().get('Site') + '"]\n')
            f.write('[Date "' + self.getMetadata().get('Date') + '"]\n')
            f.write('[Round "' + self.getMetadata().get('Round') + '"]\n')
            f.write('[White "' + self.getMetadata().get('White') + '"]\n')
            f.write('[Black "' + self.getMetadata().get('Black') + '"]\n')
            f.write('[Result "' + self.getMetadata().get('Result') + '"]\n')
            f.write('[ECO "' + self.getMetadata().get('ECO') + '"]\n')
            f.write('[Opening "' + self.getMetadata().get('Opening') + '"]\n')
            if self.getMetadata().get('Variation') != None:
                f.write(
                    '[Variation "' + self.getMetadata().get('Variation') + '"]\n')
            f.write('[PlyCount "' + self.getMetadata().get('PlyCount') + '"]\n')
            f.write('[WhiteElo "' + self.getMetadata().get('WhiteElo') + '"]\n')
            f.write('[BlackElo "' + self.getMetadata().get('BlackElo') + '"]\n\n')

            for i, move in enumerate(self.getMoves()):
                i = i + 1
                if i % 5 == 0:
                    f.write("\n")
                f.write(str(i)+". " + str(move) + ' ')
            f.write(self.getMetadata().get('Result'))


def main():
    game = ChessGame()
    # game.importFromText(
    # "/Users/christian/performanceengineering/Task 2/Database/Stockfish_15_64-bit.commented.[2600].pgn")
