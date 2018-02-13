from random import randint
from copy import deepcopy
def Generate_Map(xlength,ylength):
    '''
    Creates a random map with xlength and ylength as dimensions
    '''
    Map = []
    for i in range(ylength): #Create a blank 2D array with xlength and ylength dimensions
        Map.append([])
        for j in range(xlength):
            Map[i].append(' ')

    for i in range(ylength): #Turns every outer cell in the map into a wall
        for j in range(xlength):
            if i == 0 or j == 0 or j == xlength-1 or i == ylength-1:
                Map[i][j] = 'W'
                
    while True: #Creates maps until map is useable
        tempMap = deepcopy(Map) #Creates a copy of the map to edit
        tempMap = Generate_Path(tempMap, xlength, ylength) #Run Generate_Map, get a map with a path
        pathTF = Path_Check(tempMap, ylength, xlength) #Run pathTF, check pathways
        if pathTF:
            break
    
    Map = tempMap
    
    for i in range(ylength-1): #Populate the map with walls
        for j in range(xlength-1):
            wallVal = randint(1,100)
            if wallVal >= 60 and Map[i][j] == ' ': #40% chance of a wall being placed on an empty spot
                Map[i][j] = 'W'

    for i in range(ylength): #Goes through each cell
        for j in range(xlength):
            if Map[i][j] == 'P': #Looks for pathway marks and clears pathway cells
                Map[i][j] = ' '
    
    return Map


def Generate_Path(tMap, xlength, ylength):
    '''
    Generates a start end & path for a map given dimensions and an empty map array
    '''
    startx = randint(1,xlength-2) #Create a random start point
    starty = randint(1,ylength-2)
    endx = randint(1,xlength-2) #Create a random end point
    endy = randint(1,ylength-2)
    while startx == endx or starty == endy: #Ensure start and end point are not in the same row/columns
        endx = randint(1,xlength-2)
        endy = randint(1,ylength-2)
    tMap[starty][startx] = 'S' #Mark start
    tMap[endy][endx] = 'E' #Mark end

    pathx = startx #Start pathway coordinates
    pathy = starty

    while pathx != endx or pathy != endy: #Find a path whilst not at the endpoint
        dirVal = randint(0,1) #Whether to travel horizontal or vertical
        if dirVal == 0: #Move horizontally towards target
            if pathx > endx:
                pathx -= 1
                tMap[pathy][pathx] = 'P' #Mark path point
            elif pathx < endx:
                pathx += 1
                tMap[pathy][pathx] = 'P'
        else: #Move vertically towards target
            if pathy > endy:
                pathy -= 1
                tMap[pathy][pathx] = 'P'
            elif pathy < endy:
                pathy += 1
                tMap[pathy][pathx] = 'P'
        
    tMap[endy][endx] = 'E' #Remark end ('P' overlaps)
    tMap[starty][startx] = 'S' #Remark start ('P' overlaps)
    return tMap #Returns map with path between start and end

def Path_Check(tMap, ylength, xlength):
    '''
    Check whether tMap has a suitable pathway given y dimension
    '''
    pathCount = 0
    for i in range(ylength-1): #Counts 'P' (pathway markers)
        pathCount += tMap[i].count('P')
    maxi = int((xlength+ylength)/2) #Set max length to the average of the dimensions
    mini = int(maxi/4) #Set min length to a quarter of the average
    if pathCount > mini and pathCount < maxi: #Minimum path is between min and max lengths
        return True
    else:
        return False
