from astar import astar

direct = {
    ( 0,  1) : "N",
    ( 1,  0) : "E",
    ( 0, -1) : "S",
    (-1,  0) : "W",
    ( 1,  1) : "NE",
    ( 1, -1) : "SE",
    (-1, -1) : "SW",
    (-1,  1) : "NW",
    ( 0,  0) : None,
}

algorithms = {
    'astar' : astar,
}


#Convert Matix Coordinates to Cartesian Coordinates
def matrixToCartesian(coord, max) :
    x_coord, y_coord = coord[1], max-coord[0]
    return (x_coord, y_coord)

#Convert Cartesian Coordinate to Matrix Coordinates
def cartesianToMatrix(coord, max) :
    x_coord, y_coord = max-coord[1], coord[0]
    return(x_coord, y_coord)

#Return the difference between two tuples as a tuple
def diff(tup1, tup2) :
    rtup = []

    for i in range(len(tup1)) :
        rtup.append(tup2[i] - tup1[i])

    return tuple(rtup)

#Make all the agents to have path lists of same length
def fixPathLengths(paths) :
    lengths = []

    for path in paths :
        lengths.append(len(path))

    maxLen = max(lengths)

    for i in range(len(paths)) :
        for j in range( len(paths[i]), maxLen ) :
            paths[i].append(paths[i][j-1])

    return paths

#Check if the starting and or ending coordinates are valid or not
def isValid(maze:list, starts:list, ends:list) :
    if len(starts) != len(ends) :
        return False

    return True

#If two paths intersect at the same time, make one agent wait for other
def resolveConflicts(paths:list) :
    for j in range(len(paths[0])) :
        temp = paths[0][j]
        conIndex = None
        for i in range(1, len(paths)) :
            if temp == paths[i][j] :
                conIndex = i

    if conIndex != None :
            paths[j].insert(conIndex, paths[j][conIndex-1])

    paths = fixPathLengths(paths)
    return paths

#Get a 2D list of paths of all the agents
def getPaths(maze:list, starts:list, ends:list, algo:str) :
    paths = []
    maxMat = len(maze) - 1
    
    #Make 'func' equal to the function of required algorithm, default to astar
    try :
        func = algorithms[algo]
    except :
        print("Invalid Algorithm '" + algo + "', using astar instead")
        func = astar

    #Fetch and Store Paths in a 2D List
    for i in range(len(starts)) :
        path = []

        if algo == "astar" :
            path = func(maze, starts[i], ends[i])

        paths.append(path)
    
    #Convert Path Coordinates (Matrix) to Cartesian Coordinates
    for i in range(len(paths)) :
        for j in range(len(paths[i])) :
            paths[i][j] = matrixToCartesian(paths[i][j], maxMat)

    paths = fixPathLengths(paths)
    paths = resolveConflicts(paths)
    return paths

#Get a 2D List of individual directions for all agents
def getDirections(maze:list, starts:list, ends:list, algo:str = 'astar') :
    paths = []
    allDirections = []
    maxMat = len(maze) - 1
    noOfAgents = 0

    #Convert start and end coords to Matrix Coords
    for i in range(len(starts)) :
        starts[i] = cartesianToMatrix(starts[i], maxMat)
    for i in range(len(ends)) :
        ends[i] = cartesianToMatrix(ends[i], maxMat)

    #Check for validity of provided coordinates
    if isValid(maze, starts, ends) :
        noOfAgents = len(starts)

    paths = getPaths(maze, starts, ends, algo)
    
    #Convert Paths into a List of Individual Directions
    for i in range(len(paths[0]) - 1) :
        directions = []

        for j in range(noOfAgents) :
            directions.append(direct[diff(paths[j][i], paths[j][i+1])])

        allDirections.append(directions)

    return allDirections