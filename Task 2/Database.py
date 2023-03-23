
import collections
import ChessGame
import re
import time
import Move
import DocumentWriter
import matplotlib.pyplot as plt
import math


### IMPORTANT!!!! NEED TO COMMENT OUT IMPORT TREESTRUCTURE IF YOU ARE GOING TO RUN MAIN METHOD IN DATABASE.PY######

#import TreeStructure

####IMPORTANT!!!! NEED TO COMMENT OUT IMPORT TREESTRUCTURE IF YOU ARE GOING TO RUN MAIN METHOD IN DATABASE.PY######


class Database():

    def __init__(self, name):
        self.name = name
        self.games = []
        self.document = DocumentWriter.DocumentWriter(self.name, self.name)

    def getName(self) -> str:
        return self.name

    def setName(self, name):
        self.name = name

    def getGames(self):
        return self.games

    def getAmountOfGames(self):
        return len(self.games)

    def addGame(self, game):
        self.getGames().append(game)

    def getDocument(self):
        return self.document

    def getMetadataFromGameFile(self, game):
        # Henter inn metadata
        meta = re.findall(r'"([^"]+)"', game)

        metadata = {}
        metadata['Event'] = meta[0]
        metadata['Site'] = meta[1]
        metadata['Date'] = meta[2]
        metadata['Round'] = meta[3]
        metadata['White'] = meta[4]
        metadata['Black'] = meta[5]
        metadata['Result'] = meta[6]
        metadata['ECO'] = meta[7]
        metadata['Opening'] = meta[8]
        # Check if there is a variation, since it is optional and it will be plycount if not
        if str(meta[9]).isdigit():
            metadata['PlyCount'] = meta[9]
            metadata['WhiteElo'] = meta[10]
            metadata['BlackElo'] = meta[11]
            meta = meta[12:]
        else:
            metadata['Variation'] = meta[9]
            metadata['PlyCount'] = meta[10]
            metadata['WhiteElo'] = meta[11]
            metadata['BlackElo'] = meta[12]
            meta = meta[13:]
        return metadata

    # One file
    def getMovesFromFile(self, game):
        # Henter inn alle trekkene
        s = re.sub(r'\[[^]]+\]', '', game)
        moves_list = re.split(r'\d+\.\s+(\S+)', s)[1:]

        # Fjerner tomme elementer
        moves_list_clean = [move.lstrip().rstrip() for move in moves_list]
        # Splitter alle trekkene i toer
        moves = [moves_list_clean[i:i+2]
                 for i in range(0, len(moves_list_clean), 2)]
        # Removes the last element, since its not a move
        moves[-1].pop()
        # Returns the list of moves
        return moves

    # Task 2

    # Works for one file
    def importFromPGN(self, file):
        # Importere hele fila, og splitte i antall games
        with open(file) as f:
            game = f.read()
            # Fjerner linjeskift
            games = game.split("\n\n")
            for i in range(0, len(games)-1, 2):
                game = games[i]+games[i+1]
                game = (re.sub(r'\n', ' ', game))
            # Fjerner kommentarer
                game = (re.sub(r'\{.*?\}', '', game))
                Chessgame = self.importFromText(game)
                self.addGame(Chessgame)

    def importFromText(self, game):
        Chessgame = ChessGame.ChessGame({}, [])

        # Setting metadata
        metadata = self.getMetadataFromGameFile(game)
        Chessgame.setMetadata(metadata)
        # Setting moves
        for move in self.getMovesFromFile(game):
            try:
                Chessgame.addMove(move[0], move[1])
            except IndexError:
                Chessgame.addMove(move[0], None)
        return Chessgame
        # Creating the game

        # Split the remaining string by space

    def getGamesStockfish(self):
        wWon = 0
        wDraw = 0
        wLost = 0
        bWon = 0
        bDraw = 0
        bLost = 0
        wWonGames = []
        wDrawGames = []
        wLostGames = []
        bWonGames = []
        bDrawGames = []
        bLostGames = []

        for game in self.games:
            if game.getMetadata()['White'] == 'Stockfish 15 64-bit':
                if game.getMetadata()['Result'] == '1-0':
                    wWon += 1
                    wWonGames.append(game)
                elif game.getMetadata()['Result'] == '1/2-1/2':
                    wDraw += 1
                    wDrawGames.append(game)
                elif game.getMetadata()['Result'] == '0-1':
                    wLost += 1
                    wLostGames.append(game)
            elif game.getMetadata()['Black'] == 'Stockfish 15 64-bit':
                if game.getMetadata()['Result'] == '1-0':
                    bLost += 1
                    bLostGames.append(game)
                elif game.getMetadata()['Result'] == '1/2-1/2':
                    bDraw += 1
                    bDrawGames.append(game)
                elif game.getMetadata()['Result'] == '0-1':
                    bWon += 1
                    bWonGames.append(game)
        W = wWon + bWon
        WGames = wWonGames + bWonGames
        D = wDraw + bDraw
        DGames = wDrawGames + bDrawGames
        L = wLost + bLost
        LGames = wLostGames + bLostGames
        # print('White won:', wWon, 'White draw:', wDraw, 'White lost:', wLost)
        # print('Black won:', bWon, 'Black draw:', bDraw, 'Black lost:', bLost)
        # print('Total won:', W, 'Total draw:', D, 'Total lost:', L)
        return [[[str(W), str(D), str(L)]], [[str(wWon), str(wDraw), str(wLost)]], [[str(bWon), str(bDraw), str(bLost)]], [wWonGames, wDrawGames, wLostGames, bWonGames, bDrawGames, bLostGames, WGames, DGames, LGames]]

    def addTable(self, data, headers):
        self.getDocument().addTable(data, headers)
        self.getDocument().save()

    def gamesLeft(self, games):
        freq = []
        for game in games:
            freq.append(game.numberOfMoves())
        frequency = collections.Counter(freq)
        data = [frequency.keys(), frequency.values()]
        self.figure1('gamesLeft', 'Number of moves', 'Games left', data)
        return data

    def figure1(self, filename, xlabel, ylabel, data):
        plt.bar(data[0], data[1])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(str(filename) + '.png')
        plt.clf()

    def calculateAverage(self, games):
        tot = 0
        for game in games:
            tot += game.numberOfMoves()
        average = round(tot/len(games), 3)
        return average

    def calculateStandardDeviation(self, games):
        average = self.calculateAverage(games)
        standardDeviation = 0
        for game in games:
            standardDeviation += (game.numberOfMoves()-average)**2
        standardDeviation = standardDeviation/len(self.games)
        standardDeviation = math.sqrt(standardDeviation)
        standardDeviation = round(standardDeviation, 3)
        return standardDeviation

     # Need to extract openings played more than N times

    def extractOpenings(self, games, N):
        # Need to count frequency of openings
        openings = {}  # Dictionary of openings
        for game in games:
            opening = game.getOpening()
            if opening is not None:
                if opening not in openings:
                    openings[opening] = 1
                else:
                    openings[opening] += 1

        # Filter the opening frequencies by count
        filtered_openings = {opening: count for opening,
                             count in openings.items() if count >= N}

        return filtered_openings

    def task7(self):
        self.getDocument().addHeading("Task 7", 1)
        self.getDocument().addParagraph(
            "The table below shows the amount of games won, drawn and lost by Stockfish 15 64-bit")
        self.addTable((self.getGamesStockfish()[0]), ['Won', 'Draw', 'Lost'])
        self.getDocument().addParagraph(
            "The table below shows the amount of games won, drawn and lost by Stockfish 15 64-bit as white")
        self.addTable(list(self.getGamesStockfish()[1]), [
                      'Won', 'Draw', 'Lost'])
        self.getDocument().addParagraph(
            "The table below shows the amount of games won, drawn and lost by Stockfish 15 64-bit as black")
        self.addTable(list(self.getGamesStockfish()[2]), [
                      'Won', 'Draw', 'Lost'])
        self.getDocument().save()

    def task8_2(self):
        #
        movesWithStockfishBlack = []
        movesWithStockfishWhite = []
        movesLeft = []
        for game in self.games:
            movesLeft.append(game.numberOfMoves())
            if game.getMetadata()['Black'] == 'Stockfish 15 64-bit':
                movesWithStockfishBlack.append(game.numberOfMoves())
            elif game.getMetadata()['White'] == 'Stockfish 15 64-bit':
                movesWithStockfishWhite.append(game.numberOfMoves())

        movesLeft = collections.Counter(movesLeft)

        MovesWithStockfishBlackCol = collections.Counter(
            movesWithStockfishBlack)
        MovesWithStockfishWhiteCol = collections.Counter(
            movesWithStockfishWhite)
        MovesAll = collections.Counter(movesLeft)

        sortedMovesWithStockfishWhite = []
        for i in range(len(MovesWithStockfishWhiteCol)):
            sortedMovesWithStockfishWhite.append(
                MovesWithStockfishWhiteCol.get(i))

        sortedMovesAll = []
        for j in range(len(MovesAll)):
            sortedMovesAll.append(MovesAll.get(j))

        sortedMovesWithStockfishBlack = []
        for k in range(len(MovesWithStockfishBlackCol)):
            sortedMovesWithStockfishBlack.append(
                MovesWithStockfishBlackCol.get(k))

        plt.clf()
        plt.plot(range(len(sortedMovesAll)),
                 sortedMovesAll, '-', label='All games')
        plt.plot(range(len(sortedMovesWithStockfishWhite)),
                 sortedMovesWithStockfishWhite, '-', label='Stockfish as white')
        plt.plot(range(len(sortedMovesWithStockfishBlack)),
                 sortedMovesWithStockfishBlack, '-', label='Stockfish as black')
        plt.legend()
        plt.xlabel('Number of moves')
        plt.ylabel('Games left')
        plt.savefig("task8_2.png")
        return [movesLeft, movesWithStockfishBlack, movesWithStockfishWhite]

    def task8_3(self):
        average = ['Average']
        standardDeviation = ['Standard Deviation']
        for gamelist in self.getGamesStockfish()[3]:
            average.append(str(self.calculateAverage(gamelist)))
            standardDeviation.append(
                str(self.calculateStandardDeviation(gamelist)))
        self.getDocument().addHeading(
            "Average and Standard Deviation for all Stockfish games", 2)
        header = ['', 'White won', 'White draw', 'White lost', 'Black won',
                  'Black draw', 'Black lost', 'Total won', 'Total draw', 'Total lost']
        self.getDocument().addTable([average, standardDeviation], header)

    def task8(self):
        self.getDocument().addSection()
        self.getDocument().addHeading("Task 8", 1)
        # All games
        self.gamesLeft(self.games)
        self.getDocument().addParagraph(
            "The graph below shows the amount of games left for Stockfish 15 64-bit after x moves")
        self.getDocument().addPicture('gamesleft.png', 6)

        self.getDocument().addParagraph(
            "The graph below shows the amount of games left for Stockfish after moves, with Black, White and all games in the same plot")
        self.task8_2()
        self.getDocument().addPicture('task8_2.png', 6)
        # All games
        allAvg = self.calculateAverage(self.games)
        allStd = self.calculateStandardDeviation(self.games)
        self.task8_3()

    def task11(self):
        self.getDocument().addSection()
        self.getDocument().addHeading("Task 11", 1)
        self.getDocument().addParagraph("The graphs below are openings from all games in the database. It will display all possible openings with a specified depth in the function. In this case, the depth is 5")
        TreeManagement = TreeStructure.TreeManagement()
        TreeManagement.addGames(TreeManagement.importMoves(
            file="/Users/christian/performanceengineering/Task 2/Database/Stockfish_15_64-bit.commented.[2600] 2.pgn"), depth=5)
        # Creates png files for all openings
        TreeManagement.visualize_opening_trees()

        self.getDocument().addPicture('b3_tree.png', 6)
        self.getDocument().addParagraph("b3 opening")
        self.getDocument().addPicture('b4_tree.png', 6)
        self.getDocument().addParagraph("b4 opening")
        self.getDocument().addPicture('c4_tree.png', 1.5)
        self.getDocument().addParagraph("c4 opening")
        self.getDocument().addPicture('d3_tree.png', 6)
        self.getDocument().addParagraph("d3 opening")
        self.getDocument().addPicture('d4_tree.png', 1.2)
        self.getDocument().addParagraph("d4 opening")
        self.getDocument().addPicture('e4_tree.png', 1.2)
        self.getDocument().addParagraph("e4 opening")
        self.getDocument().addPicture('f4_tree.png', 6)
        self.getDocument().addParagraph("f4 opening")
        self.getDocument().addPicture('g3_tree.png', 6)
        self.getDocument().addParagraph("g3 opening")
        self.getDocument().addPicture('Nc3_tree.png', 6)
        self.getDocument().addParagraph("Nc3 opening")
        self.getDocument().addPicture('Nf3_tree.png', 1.4)
        self.getDocument().addParagraph("Nf3 opening")

    def task12(self):
        self.getDocument().addSection()
        self.getDocument().addHeading("Task 12", 1)
        self.getDocument().addParagraph("The table below shows the amount openings played. The table is automatically created with all openings played more than N times. N is set to 50 in this case.")
        data = []
        openings = self.extractOpenings(self.games, 50)
        openings = sorted(openings.items(), key=lambda x: x[-1], reverse=True)
        for key, value in openings:
            key1 = []
            value1 = []
            key1.append(str(key))
            value1.append(str(value))
            data.append(key1 + value1)

        self.getDocument().addTable(data, ['Opening', 'Frequency'])

    def createDocument(self):
        self.task7()
        self.task8()
        self.task11()
        self.task12()
        self.getDocument().save()


def main():
    import TreeStructure
    st = time.time()
    db = Database("Chess Database")
    db.importFromPGN(
        "/Users/christian/performanceengineering/Task 2/Database/Stockfish_15_64-bit.commented.[2600] 2.pgn")
    db.createDocument()
    db.extractOpenings(db.games, 50)

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


if __name__ == "__main__":
    main()
