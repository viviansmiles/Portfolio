from random import randint
from copy import deepcopy
def Generate_Map(xlength,ylength):
    '''
    Creates a random map with xlength and ylength as dimensions
    Takes map dimensions as input
    '''
    
    #Create a 2D array with xlength and ylength dimensions filled with empty (' ') cells
    Map = []
    for i in range(ylength): 
        Map.append([])
        for j in range(xlength):
            Map[i].append(' ')

    #Turns every outer cell in the map into a wall
    for i in range(ylength): 
        for j in range(xlength):
            if i == 0 or j == 0 or j == xlength-1 or i == ylength-1:
                Map[i][j] = 'W'
                
    #Creates usable maps and determines start/end points with a path
    while True: 
        tempMap = deepcopy(Map) #Creates a copy of the map to edit
        tempMap = Generate_Path(tempMap, xlength, ylength) #Get a map with a path
        pathTF = Path_Check(tempMap, ylength, xlength) #Check pathways
        if pathTF:
            break
    Map = tempMap
    
    #Populate the map with walls
    for i in range(ylength-1):
        for j in range(xlength-1):
            wallVal = randint(1,100)
            if wallVal >= 60 and Map[i][j] == ' ': #40% chance of a wall being placed on an empty spot
                Map[i][j] = 'W'

    #Goes through each cell and removes pathway markers ('P')
    for i in range(ylength): 
        for j in range(xlength):
            if Map[i][j] == 'P':
                Map[i][j] = ' '
    
    return Map


def Generate_Path(tMap, xlength, ylength):
    '''
    Generates a start end & path for a map given dimensions and an empty map array
    Takes temporary map, length and width as input
    '''
    
    #Create a random start and end point
    startx = randint(1,xlength-2) 
    starty = randint(1,ylength-2)
    endx = randint(1,xlength-2)
    endy = randint(1,ylength-2)
    
    #Ensure start and end point are not in the same row/columns
    while startx == endx or starty == endy: 
        endx = randint(1,xlength-2)
        endy = randint(1,ylength-2)
    tMap[starty][startx] = 'S' #Mark start
    tMap[endy][endx] = 'E' #Mark end

    
    pathx = startx 
    pathy = starty
    #Find a path whilst not at the endpoint
    while pathx != endx or pathy != endy: 
        dirVal = randint(0,1)
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
    Takes map, width and length as input
    '''
    
    #Ensures pathway is suitable by checking path length
    pathCount = 0
    for i in range(ylength-1): #Counts 'P' (pathway markers)
        pathCount += tMap[i].count('P')
    
    maxi = int((xlength+ylength)/2) #Set max length to the average of the dimensions
    mini = int(maxi/4) #Set min length to a quarter of the average
    
    #Ensures path is between min and max lengths
    if pathCount > mini and pathCount < maxi: 
        return True
    else:
        return False
