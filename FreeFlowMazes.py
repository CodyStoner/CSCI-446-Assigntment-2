from collections import defaultdict
import mazes
import random
import heapq




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
        mazes.printMaze(maze)


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
            mazes.printMaze(assignment)
            return assignment

        node = self.getNode(assignment) #get a node that has not been visited

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

    def backtracking(self, assignment):
        pass

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

if __name__=='__main__':
    #create mazes
    mazeTest = mazes.readMaze("5x5maze_solution.txt")
    maze5x5 = mazes.readMaze("5x5maze.txt")
    maze7x7 = mazes.readMaze("7x7maze.txt")
    maze8x8 = mazes.readMaze("8x8maze.txt")
    maze9x9 = mazes.readMaze("9x9maze.txt")
    maze10x10 = mazes.readMaze("10x10maze.txt")
    maze12x12 = mazes.readMaze("12x12maze.txt")
    maze14x14 = mazes.readMaze("14x14maze.txt")

    print("Solving 5x5:")
    csp5x5 = CSP(maze5x5)
    csp5x5.dumbBacktracking(maze5x5)

    cspmazeTest = CSP(mazeTest)#Prints out the correct maze given by instructor

    print("Solving 7x7:")
    csp7x7 = CSP(maze7x7)
    csp7x7.dumbBacktracking(maze7x7)

    print("Solving 8x8:")
    csp8x8 = CSP(maze8x8)
    csp8x8.dumbBacktracking(maze8x8)

    print("Solving 9x9:")
    csp9x9 = CSP(maze9x9)
    csp9x9.dumbBacktracking(maze9x9)

    print("Solving 10x10:")
    csp10x10 = CSP(maze10x10)
    csp10x10.dumbBacktracking(maze10x10)
    
