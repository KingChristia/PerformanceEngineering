import time
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from IPython.display import Image, display


# IMPORTANT!!! NEED TO COMMENT OUT DATABASE IF YOU CHOOSE TO RUN DATABASE MAIN FUNCTION!

import Database

# IMPORTANT!!! NEED TO COMMENT OUT DATABASE IF YOU CHOOSE TO RUN DATABASE MAIN FUNCTION!

class Node:
    _id_counter = 0

    def __init__(self, move, turn=None, depth=0, parent=None, opening=None):
        self.id = Node._id_counter
        Node._id_counter += 1
        self.turn = turn
        self.parent = parent
        self.children = {}
        self.outcomes = {'white': 0, 'black': 0, 'draw': 0}
        self.move = move
        self.previousMoves = (self.parent.previousMoves +
                              [self.move]) if self.parent is not None else [self.move]
        self.depth = depth
        self.opening = opening

    def addOutcome(self, outcome):
        if outcome == 'draw':
            self.outcomes['draw'] += 1
        else:
            self.outcomes[outcome.lower()] += 1

    def getDepth(self):
        return self.depth

    def setTurn(self, turn):
        self.turn = turn

    def getChild(self, move):
        return self.children.get(move)

    def getMove(self):
        return self.move

    def setDepth(self):
        self.depth = self.parent.getDepth() + 1

    def addChild(self, move, child):
        self.children[move] = child

    def __str__(self) -> str:
        return f"Node: {self.move} \nDepth: {self.depth} \nTurn: {self.turn} \nOutcomes: {self.outcomes} \nPrevious Moves: {self.previousMoves} \nChildren: {self.children}"


class Tree:
    _id_counter = 0

    def __init__(self, rootNode):
        self.root = rootNode
        rootNode.setTurn('white')
        #
        self.root.id = Tree._id_counter
        Tree._id_counter += 1
        self.nodes = {}  # {Node: depth}
        self.rootOutcome = None

    def addGame(self, moves, outcome):
        node = self.root
        for i, move in enumerate(moves):
            player = 'black' if i % 2 == 0 else 'white'
            parent = node

            # Check if the move already exists as a child of the current node
            existing_child = None
            for child in node.children.values():
                if child.move == move:
                    existing_child = child
                    break

            # If the move exists, update the existing child node and its outcomes
            if existing_child:
                node = existing_child
            else:
                # If the move does not exist, create a new child node
                new_child = Node(move=move, turn=player, parent=parent)
                new_child.setDepth()
                node.children[len(node.children)] = new_child
                node = new_child

            node.addOutcome(outcome)
        self.root.outcomes = self.get_depth1_outcomes()

    # Sum the outcomes from all nodes in depth 1

    def get_depth1_outcomes(self):
        depth1_outcomes = {'white': 0, 'black': 0, 'draw': 0}

        for child in self.root.children.values():
            for outcome, count in child.outcomes.items():
                depth1_outcomes[outcome] += count

        return depth1_outcomes

    def visualize(self, output_file_name="tree.png"):
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')
        self._add_node_edges_to_graph(self.root, graph)
        graph.write_png(output_file_name)

    def _add_node_edges_to_graph(self, node, graph):
        if not node:
            return

        # Set the node color based on the turn
        # Set root node

        if node.turn.lower() == 'white':
            node_color = 'white'
        elif node.turn.lower() == 'black':
            node_color = 'black'

        # Include the opening name for the root node
        if node.depth == 1 and node.opening:
            node_label = f"{node.opening}\n{node.move}\n{node.depth}\nW: {node.outcomes['white']} D: {node.outcomes['draw']} B: {node.outcomes['black']}"
        else:
            node_label = f"{node.move}\n{node.depth}\nW: {node.outcomes['white']} D: {node.outcomes['draw']} B: {node.outcomes['black']}"

        graph_node = pydot.Node(str(node.id), label=node_label, shape='ellipse', style='filled',
                                fillcolor=node_color, fontcolor='black' if node_color == 'white' else 'white')
        graph.add_node(graph_node)
        for child in node.children.values():
            edge = pydot.Edge(str(node.id), str(child.id))
            graph.add_edge(edge)
            self._add_node_edges_to_graph(child, graph)

    def getRoot(self):
        return self.root


class TreeManagement:
    def __init__(self) -> None:
        self.trees = {}


    def addGame(self, moves, depth, outcome, opening):
        if moves[0] not in self.trees:
            self.trees[moves[0]] = Tree(
                Node(moves[0], opening=opening, turn='white'))
        self.trees[moves[0]].addGame(moves[1:depth], outcome)

    def addGames(self, games, depth):
        for game, moves in games.items():
            self.addGame(moves, depth, game.getWinningColor(),
                         game.getOpening())

    def getTree(self, move):
        return self.trees.get(move)

    def getAmountOfTrees(self):
        return len(self.trees)

    # Returnerer en liste for hver game med alle moves
    def importMoves(self, file):
        gameMovesList = {}

        db = Database.Database("Test")
        db.importFromPGN(file)
        # cleaner moves til riktig format for senere
        for game in db.getGames():
            gameMoves = []
            for i in range(len(game.getMoves())):
                gameMoves.append(game.getMoves()[i].getFirstMove())
                gameMoves.append(game.getMoves()[i].getSecondMove())
            gameMoves.pop()
            gameMovesList[game] = gameMoves
        return gameMovesList

    def visualize_opening_trees(self):
        for opening, tree in self.trees.items():
            tree.visualize(f"{opening}_tree.png")


def main():
    st = time.time()
    treeManagement = TreeManagement()
    db = "/Users/christian/performanceengineering/Task 2/Database/Stockfish_15_64-bit.commented.[2600] 2.pgn"
    # (treeManagement.importMoves(db))
    
    ####CREATES THE TREE FILES AS PGN
    treeManagement.addGames(treeManagement.importMoves(db), 130)
    treeManagement.visualize_opening_trees()
    ####

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


main()
