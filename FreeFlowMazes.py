from collections import defaultdict
import mazes
import random
import heapq
import time
import argparse
import sys
import copy
from pathlib import Path

class CSP:
    def __init__(self, maze):
        self.domain = []
        self.start = {}
        self.finish = {}
        self.visited = []
        self.colorVisited = defaultdict(list)
        self.island = []
        self.completeColors = []
        self.findStartandFinish(maze)
        self.variableAssignments = 0
        self.t_start = time.time()


    def findStartandFinish(self, maze): #find start and finish to each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    self.visited.append(node) #append to visited so their values do not change
                    if node.value not in self.domain:
                        self.domain.append(node.value)
                    if node.value not in self.start:
                        self.start[node.value] = node
                        self.colorVisited[node.value].append(node)
                    else:
                        self.finish[node.value] = node
                        self.colorVisited[node.value].append(node)

    def dumbBacktracking(self, assignment):
        if self.complete(assignment): #if the assignment is complete, return and print maze
            print("Var. Assignments:", self.variableAssignments, ", Time: ", time.time() - self.t_start)
            mazes.printMaze(assignment)
            return assignment

        node = self.getNode(assignment) #get a node that has not been visited
        self.variableAssignments += 1

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False
        
        if len(self.island) > 0:
            for icolor in self.island:
                if self.hasIsland(icolor, self.colorVisited[icolor]):
                    return False
                else:
                    self.island.remove(icolor)

        for color in self.getColors(node):
            if self.consistant(color, node, assignment): #if the color we have chosen is legal, use it
                self.visited.append(node)
                self.colorVisited[color].append(node)
                result = self.dumbBacktracking(assignment) #move on to next node
                if result:
                    return result
                self.visited.remove(node) #that branch failed, backtrack
                self.colorVisited[color].remove(node)
                if color in self.completeColors:
                    self.completeColors.remove(color)
                node.value = '_'
        return False

    def smartBacktracking(self, assignment):
        if self.complete(assignment): #if the assignment is complete, return and print maze
            print("Var. Assignments:", self.variableAssignments, ", Time: ", time.time() - self.t_start)
            mazes.printMaze(assignment)
            return assignment

        node = self.getNode_i(assignment) #get a node that has not been visited
        self.variableAssignments += 1

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False
        
        if len(self.island) > 0:
            for icolor in self.island:
                if self.hasIsland(icolor, self.colorVisited[icolor]):
                    return False
                else:
                    self.island.remove(icolor)

        for color in self.getColors(node):
            if self.consistant(color, node, assignment): #if the color we have chosen is legal, use it
                self.visited.append(node)
                self.colorVisited[color].append(node)
                result = self.smartBacktracking(assignment) #move on to next node
                if result:
                    return result
                self.visited.remove(node) #that branch failed, backtrack
                self.colorVisited[color].remove(node)
                if color in self.completeColors:
                    self.completeColors.remove(color)
                node.value = '_'
        return False

    def getColors(self, node):
        colors = [] #prioitizes adjacent colors
        for neighbor in node.neighbors:
            if neighbor.value is not '_' and neighbor.value not in colors and neighbor.value not in self.completeColors:
                colors.append(neighbor.value)
        for color in self.domain:
            if color not in colors and color not in self.completeColors:
                colors.append(color)
        return colors

    def getNode(self, assignment):
        for row in assignment:
            for node in row:
                if node not in self.visited: #if node is not visited, return
                    return node

    def getNode_i(self, assignment):
        bestNode = None
        paths = 0
        for row in assignment:
            for node in row:
                if node not in self.visited: #if node is not visited, check if it is better than bestNode
                    nodePaths = 0;
                    pathNear = False
                    for neighbor in node.neighbors:
                        if neighbor not in self.visited and neighbor.value is '_':
                            nodePaths += 1

                        if neighbor.value is not '_':
                            pathnear = True

                    if bestNode is None or (nodePaths != 0 and nodePaths < paths and pathNear):
                        bestNode = node
                        paths = nodePaths

                    if paths == 1 and pathNear:
                        return bestNode
        return bestNode

    def complete(self, assignment): #checks to see if assignment is correct
        for color in self.domain:
            if color not in self.completeColors:
                return False
        print('Completed Maze')
        return True

    def consistant(self, color, node, assignment):
        node.value = color

        #if the node will not cause a zig_zag, the start and finish node only have one child, and we dont corner any other nodes, move on
        for neighbor in node.neighbors:
            if neighbor.value is not '_':
                if self.zigZag(neighbor, color) or not self.startFinishCons(neighbor, color) or self.cornered(neighbor) or not self.colorPartcompleteStart(neighbor.value) or not self.colorPartcompleteFinish(neighbor.value):
                    node.value = '_'
                    return False

        localComplete, path = self.colorComplete(color)
        if localComplete:
            self.completeColors.append(color)
            if self.hasIsland(color, path):
                self.island.append(color)
        return True

    def zigZag(self, node, color):
        if node.value is color:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1
                if count > 2:
                    return True
        return False

    def startFinishCons(self, node, color):
        if node is self.start[color] or node is self.finish[color]:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1
                if count >= 2:
                    return False
        return True

    def cornered(self, node):
        if not self.corneredHelp(node):
            return True
        return False

    def corneredHelp(self, node):
        for neighbor in node.neighbors: #if this node has no path to either a color or '_'
            if neighbor.value is '_' or neighbor.value is node.value:
                return True
        return False

    def colorComplete(self, color):
        node = self.start[color]#checks to see if color is complete
        path = []
        while node is not self.finish[color]:
            for neighbor in node.neighbors:
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break
                elif neighbor is node.neighbors[-1]:
                    return False, path
        return True, path

    def colorPartcompleteStart(self, color):
        node = self.start[color] #checks to see if color is part complete
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color] or neighbor.value is '_':
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    return False
        return False

    def colorPartcompleteFinish(self, color):
        node = self.finish[color] #checks to see if color is part complete
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.start[color] or neighbor.value is '_':
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    return False
        return False

    def hasIsland(self, color, path):
        for node in self.colorVisited[color]:
            if node not in path:
                return True
        return False

def solveMaze(filePath, dumb, smart):
    maze = mazes.readMaze(filePath)
    maze_i = mazes.readMaze(filePath)
    mazeCSP = CSP(maze)
    mazeCSP_i = CSP(maze_i)
    if dumb or not smart:
        print("################## Dumb ##################")
        print("Solving", filePath)
        mazes.printMaze(maze)
        mazeCSP.dumbBacktracking(maze)
    if smart or not dumb:
        print("############### Intelligent ###############")
        print("Solving", filePath)
        mazes.printMaze(maze_i)
        mazeCSP_i.smartBacktracking(maze_i)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action="store", dest="filePath", type=str, help='Solve and display a single maze')
    parser.add_argument('-d', action="store", dest="dirPath", type=str, help='Solve and display all mazes ending in .txt in given directory')
    parser.add_argument('--smart', '-S', action="store_true", default=False, help='solve mazes using only intelligent method')
    parser.add_argument('--dumb', '-D', action="store_true", default=False, help='solve mazes using only dumb method')

    if len(sys.argv[1:])==0:
        parser.print_help()
        # parser.print_usage() # for just the usage line
        parser.exit()

    args = parser.parse_args()
    filePath = args.filePath
    dirPath = args.dirPath
    dumb = args.dumb
    smart = args.smart

    if filePath:
        solveMaze(filePath, dumb, smart)

    if dirPath:
        mazePaths = Path(dirPath).glob('*.txt')
        for path in mazePaths:
            solveMaze(path, dumb, smart)
