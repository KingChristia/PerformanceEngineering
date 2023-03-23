

class Move():

    def __init__(self, move1, move2):
        # Move 1 is the white move, move 2 is the black move
        self.move1 = move1
        self.move2 = move2

    def getMoves(self):
        return self.move1, self.move2
    
    def getFirstMove(self):
        return self.move1
    
    def getSecondMove(self):
        return self.move2

    def __str__(self) -> str:
        if self.move2 != None:
            return str(self.move1 + " " + self.move2)
        else:
            return str(self.move1)
