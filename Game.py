from Display_Options import *
from Generate_Map import *
from Help import *
from random import *
from copy import deepcopy
import pickle
from Events import *
from Battles import *
from Item_Use import *
import os

def Get_Movement(playerCoord,Map,inventory):
    '''
    Gets move of player given player coordinates, inventory and map
    '''
    options = []
    if Map[playerCoord[1]-1][playerCoord[0]] != 'W': #Adds possible movements to a list
        options.append(1)
    if Map[playerCoord[1]][playerCoord[0]+1] != 'W':
        options.append(2)
    if Map[playerCoord[1]][playerCoord[0]-1] != 'W':
        options.append(3)
    if Map[playerCoord[1]+1][playerCoord[0]] != 'W':
        options.append(4)
    for item in inventory: #Checks if any actual items in the inventory
        if item != None: 
            options.append(5)
            break
    options.append(6) #Help screen
    options.append(7) #Quitting the game
    
    choice = int(Display_Options("What do you want to do? ",['North','East','West','South','Item','Help','Sleep'])) #Gets player movement choice
    while choice not in options:
        if choice >= 1 and choice <= 4:
            print("\nYou run face first into a wall.\n")
        else:
            print("\nYou reach into your bag to find... NOTHING! ABSOLUTELY NOTHING!\n")
        choice = int(Display_Options("Which way do you want to go? ",['North','East','West','South','Item','Help','Sleep'])) #Gets player movement choice

    selection = 0 #Sets selection default to 0 (move)
    if choice == 1: #Moves the player based on direction
        playerCoord = [playerCoord[0],playerCoord[1]-1]
    elif choice == 2:
        playerCoord = [playerCoord[0]+1,playerCoord[1]]
    elif choice == 3:
        playerCoord = [playerCoord[0]-1,playerCoord[1]]
    elif choice == 4:
        playerCoord = [playerCoord[0],playerCoord[1]+1]
    elif choice == 5: #Sets selection to 1 if using an item
        selection = 1
    elif choice == 6: #Sets selection to 2 if requesting help screen
        selection = 2
    else:
        selection = 3 #Sets selection to 3 if leaving

    return playerCoord,selection #Returns new coordinates and selection variable

def Get_Map(difficulty):
    '''
    Gets a map based on width and height
    '''

    if difficulty == 1: #Generates map size based off difficulty
        xlength = randint(8,13)
        ylength = randint(8,13)
    elif difficulty == 2:
        xlength = randint(14,19)
        ylength = randint(14,19)
    else:
        xlength = randint(20,25)
        ylength = randint(20,25)
    
    Map = Generate_Map(xlength,ylength) #Generates a map

    for y in range(ylength): #Marks player's coordinates
        for x in range(xlength):
            if Map[y][x] == 'S':
                playerCoord = [x,y]
    return(Map,playerCoord) #Returns map, end and starting coordinates

def Skip_Battle(save):
    '''
    Determines whether the player is able to skip battle and gives the player the option to
    Takes save as an input, updates if necessary and returns save and the skip boolean as outputs
    '''
    if Items['Milk'] in save.inventory: #If the player can skip
        skipInput = input("Do you want to use Milk and skip the battle? (y/n) ") #If the player wants to skip
        while skipInput != 'y' and skipInput != 'n':
            skipInput = input("Do you want to use Milk and skip the battle? (y/n) ")
        if skipInput == 'y':
            skip = True
        else:
            skip = False
    else:
        skip = False

    if skip: #Removing the item that skips from the inventory
        for i in range(len(save.inventory)):
            if save.inventory[i] == Items['Milk']:
                save.inventory[i] = None
                break

    return(skip,save.inventory)

def Cell_Event(save,selection):
    '''
    Determines what happens in a cell based off user selection
    Save is the save record
    Selection is the user's move on this cell (move = 0, item = 1, help = 2, quit = 3)
    '''
    if selection == 1: #If using an item
        save = Use_Item(save)
    elif selection == 3: #Saves and leave game if input is 'Sleep'
        pickle.dump(save,open("Saves/save.p","wb"))
        quit()
    else: #If moving, generate event/battle
        #cellRand = randint(0,1)
        cellRand = 1
        if cellRand == 1:
            save = Get_Event(save)
        else:
            skip,save.inventory = Skip_Battle(save)
            if skip:
                print("%s the milk drinker fled from combat. Coward." %(save.character.name))
            else:
                save = Battle(save)                
    return save #Returns resulting save

def Main_Loop(save):
    '''
    Runs main game
    '''
    while True: #Runs main loop

        for i in range(len(save.Map)):
            for j in range(len(save.Map[i])):
                if save.Map[i][j] == 'E':
                    endCoord = [j,i]
        
        while save.playerCoord != endCoord: #While player isn't at the end
            save.playerCoord,selection = Get_Movement(save.playerCoord,save.Map,save.inventory) #Gets movement
            if selection == 2:
                Show_Help()
            else:
                save = Cell_Event(save,selection)
                if save.gameOver == 0:
                    end = input("You perform an elaborate death scene for over 10 minutes, but eventually you fall. You are dead. (Press enter to quit)")
                    os.remove("Saves/save.p")
                    quit()
            if save.playerCoord == endCoord: #Breaks loop if reached end
                break
        print("You reach a large room that is entirely empty bar a small sack in the centre. You open it, and a small, sentient mushroom jumps out. \"I'm sorry, %s, but I feel like arbitrarilly extending the game length and rendering all of your previous actions pointless!\" He then magically teleports you to the start of a new dungeon." %(save.character.name))
        save.Map,save.playerCoord = Get_Map(save.difficulty) #Gets map
