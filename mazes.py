from pathlib import Path

def readMaze(filename):
    #read in file
    maze = []
    file_path = Path(filename)
    file = open(file_path, "r")
    columns = file.readlines()
    for i, column in enumerate(columns):
        column = column.strip()
        rowNodes = []
        for j, row in enumerate(column):
            for element in row:
                #make each element a node
                newNode = Node(element, i, j)
                rowNodes.append(newNode)
        maze.append(rowNodes)
    #give each node knowledge on its neighbors
    for i, row in enumerate(maze):
        for j, element in enumerate(row):
            if j+1 <= len(row)-1:
                element.neighbors.append(maze[i][j+1])
            if j-1 >= 0:
                element.neighbors.append(maze[i][j-1])
            if i-1 >= 0:
                element.neighbors.append(maze[i-1][j])
            if i+1 <= len(maze)-1:
                element.neighbors.append(maze[i+1][j])
    return maze

def printMaze(maze):
    for row in maze:
        for element in row:
            print(element.value, end='')
        print('')
    print()

class Node:
    def __init__(self, val, x, y):
        self.visited = False
        self.value = val
        self.x = x
        self.y = y
        self.neighbors = []
        self.previous = None

    def isVisited(self):
        self.visited = True
