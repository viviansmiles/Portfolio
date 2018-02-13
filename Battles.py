from random import *
from Base_Stats import *
from Create_Save import *
from Display_Options import *

def Get_Item(save):
    '''
    Gets a random item to give to the player
    Takes save as input, updates and returns as output
    '''
    itemList = []
    for itemName in Items: #Adds item names to a list a number of times to get a certain percentage chance of a certain item
        if Items[itemName].ID == 0: #Healing items (~32%)
            n = 3
        elif Items[itemName].ID == 1: #Full healing items (~7%)
            n = 3
        elif Items[itemName].ID >= 2 and Items[itemName].ID <= 6: #Stat increase items (25%)
            n = 1
        elif Items[itemName].ID == 7: #All stat increase items (~7%)
            n = 6
        elif Items[itemName].ID == 20: #Special event items (~4%)
            n = 3
        elif Items[itemName].ID >= 13 and Items[itemName].ID <= 16: #Replacement items (~10%)
            n = 2
        elif Items[itemName].ID >= 17 and Items[itemName].ID <= 18: #Extra/lose life items (~5%)
            n = 2
        elif Items[itemName].ID == 8 or Items[itemName].ID == 9 or Items[itemName].ID == 19: #Other items (~10%)
            n = 3
        else:
            n = 0
            
        for i in range(n): #Adds items to the list
            itemList.append(itemName)

    itemChance = randint(1,4) #25% chance of getting an item
    if itemChance and None in save.inventory:
        itemName = sample(itemList,1)[0]
        item = Items[itemName]
        print("You find a %s lying beside the beast's carcass!" %(itemName))
        
        for i in range(len(save.inventory)): #Adding to inventory by replacing item
            if save.inventory[i] == None:
                save.inventory[i] = item
                break

    return save.inventory

def Display_ASCII(attSpecies,defSpecies,moveType):
    '''
    Displays a line of ASCII art relating to combat
    Takes attSpecies (attacking species), defSpecies (defending species) and moveType (type of move to print) as inputs
    Displays ASCII art as output
    '''
    f = open("ASCII Art/Species/%s.txt" %(attSpecies),'r') #Loads attacking character's ASCII art
    attASCII = f.readline().strip()
    f.close()

    f = open("ASCII Art/Species/%s.txt" %(defSpecies),'r') #Loads defending character's ASCII art
    temp = f.readline() #Skips second line
    defASCII = f.readline().strip()
    f.close()

    f = open("ASCII Art/Attacks/%s.txt" %(moveType),'r') #Loads move's ASCII art
    moveASCII = f.readline().strip()
    f.close()

    if moveType == 2 or moveType == 4: #If the move doesn't affect the defender
        print("\n" + attASCII + '  ' + moveASCII)
    else:
        print("\n" + attASCII + '  ' + moveASCII + '  '+ defASCII)

    

def Apply_AA_Ability(ablChar,otrChar,attackType):
    '''
    Applies a relevant after attacking ability
    Takes ablChar (character using ability), otrChar (other character) and attackType as inputs
    Returns updated otrChar as output
    '''
    if ablChar.ability.ID == 11: #If the ability deals damage to the other character
        if attackType == 0 or attackType == 3 or attackType == 4:
            otrChar.stats[0] -= 5
            if otrChar.stats[0] < 0:
                otrChar.stats[0] = 0
            print("%s's Rough Barbs hurt %s!" %(ablChar.name,otrChar.name))

    return otrChar

def Apply_CM_Ability(ablChar,move):
    '''
    Applies a relevant change move ability
    Takes ablChar (character using ability) and move as inputs
    Modifies move if necessary and returns as output
    '''
    if ablChar.ability.ID == 13: #If the ability increases damage and recoil (10% chance)
        ablRand = randint(1,10)
        if ablRand == 1 and move.status == 0:
            move.power += 25
            move.status = 3
            move.statChange = 0
            move.secondaryStat -= 10
            print("%s's Reckless is powering up!" %(ablChar.name))

    return move
        
def Apply_DM_Ability(ablChar,otrChar,move):
    '''
    Applies a relevant damage multiplier ability
    Takes ablChar (character using ability), otrChar (other character) and move as inputs
    Determines a damage multiplier and returns as output
    '''
    ablMultiplier = 1
    otrMultiplier = 1

    if ablChar.ability.ID == 3: #If ability increases damage proportional to health lost
        healthPercentage = ablChar.stats[0]/ablChar.stats[1]
        if healthPercentage < 0.5:
            ablMultiplier = 0.5-healthPercentage + 1
        print("%s's Rampage is powering up!" %(ablChar.name))
    
    elif ablChar.ability.ID == 17: #If ability has chance for critical damage
        critChance = randint(1,5) #Determines whether critical or not
        if critChance == 1:
            ablMultiplier = 2
            print("%s's Critical Shot is locking on!" %(ablChar.name))

    if otrChar.ability.ID == 15: #If other character ability changes damage based on typing
        if move.element == 1:
            otrMultiplier = 0.25
            print("%s's Water Veil is rising!" %(otrChar.name))
        elif move.element == 2:
            otrMultiplier = 2.5
            print("%s's Water Veil is falling!" %(otrChar.name))

    damageMultiplier = ablMultiplier * otrMultiplier

    return damageMultiplier        
    

def Apply_BoB_Ability(ablChar,otrChar):
    '''
    Applies a relevant begining of battle (BoB) ability
    Takes ablChar (character using ability) and otrChar (other character) as inputs, updates and returns as outputs
    '''
    if ablChar.ability.ID == 6:
        otrChar.stats[3] *= 0.8
        otrChar.stats[3] = int(otrChar.stats[3])
        print("%s's Shadowform lowered %s's defence!" %(ablChar.name,otrChar.name))

    return(ablChar,otrChar)

def Apply_EoT_Ability(ablChar, otrChar):
    '''
    Applies a relevant end of turn (EoT) ability
    Takes ablChar (character using ability) and otrChar (other character) as inputs, updates and returns as outputs
    '''
    if ablChar.ability.ID == 4: #If the ability increases accuracy
        ablChar.stats[5] += 5
        print("%s's Clear Mist increased accuracy!" %(ablChar.name))
        
    elif ablChar.ability.ID == 7: #If the ability deals damage to the enemy
        otrChar.stats[0] -= 2
        if otrChar.stats[0] < 0:
            otrChar.stats[0] = 0
        print("%s's Dark Pulse affected %s!" %(ablChar.name,otrChar.name))
        
    elif ablChar.ability.ID == 8 and ablChar.stats[0] > 0: #If the ability restores health
        ablChar.stats[0] += 2
        if ablChar.stats[0] >= ablChar.stats[1]:
            ablChar.stats[0] = ablChar.stats[1]
        print("%s's Healing Touch restored health!" %(ablChar.name))

    elif ablChar.ability.ID == 9: #If the ability increases all stats except speed (5% chance)
        ablRand = randint(1,20)
        if ablRand == 1:
            for i in range(len(ablChar.stats)):
                if i != 4:
                    ablChar.stats[i] += 10
            print("%s's Blessing of Might increased stats!" %(ablChar.name))

    elif ablChar.ability.ID == 10: #If the ability increases defence
        ablChar.stats[3] += 2
        print("%s's Sturdy increased defence!" %(ablChar.name))

    elif ablChar.ability.ID == 12: #If the ability increases speed (5% chance)
        ablRand = randint(1,20)
        if ablRand == 1:
            ablChar.stats[4] -= 1
            if ablChar.stats[4] <= 1:
                ablChar.stats[4] = 1
            print("%s's Tailwind increased speed!" %(ablChar.name))

    elif ablChar.ability.ID == 16: #If the ability increases attack
        ablChar.stats[2] += 2
        print("%s's Supercharge increased attack!" %(ablChar.name))

    return(ablChar,otrChar)

def Apply_Turn_Ability(ablChar):
    '''
    Applies a relevant ability that causes the character to move or the opposing character to skip
    Takes ablChar (character using ability) as input and returns turn value
    '''
    turnVal = 0
    if ablChar.ability.ID == 1: #If the ability allows you to move on a turn you can't move on (5% chance)
        ablRand = randint(1,10)
        if ablRand:# == 1:
            turnVal = 1
            print("%s's Quick Recovery allows them to fight!" %(ablChar.name))

    elif ablChar.ability.ID == 5: #If the ability prevents the enemy from moving (5% chance)
        ablRand = randint(1,10)
        if ablRand == 1:
            turnVal == -1
            print("%s's Freezing Emrace froze the opponent solid!" %(ablChar.name))

    return turnVal

def Apply_AS_Ability(ablChar,attackType):
    '''
    Applies a relevant ability that causes the character to evade an attack
    Takes character using ability and attack type as inputs and returns the skip value as output
    '''
    skipVal = 0

    if ablChar.ability.ID == 0 and (attackType == 0 or attackType == 3 or attackType == 4): #If the ability prevents damage
        ablRand = randint(1,10)
        if ablRand == 1:
            skipVal = 1
            print("%s's Sharp Reflexes prevent damage!" %(ablChar.name))

    elif ablChar.ability.ID == 2 and (attackType == 2 or attackType == 4): #If the ability prevents negative stat changes
        skipVal = 2
        print("%s's White Smoke prevents stat decrease!" %(ablChar.name))

    elif ablChar.ability.ID == 14 and attackType == 5: #If the ability prevents DoT
        skipVal = 3
        print("%s's Slippery Skin prevents damage over time!" %(ablChar.name))

    return skipVal
    

def Scale_Enemy(stats,difficulty):
    '''
    Increases/decreases the stats of the enemy by 15% based on difficulty
    Takes original stats of the enemy and difficulty as inputs
    Returns updated stats as output
    '''
    if difficulty == 1: #Determines the value to multiply by
        scaleVal = 0.85
        stats[4] += 1 #Decreases speed
    else:
        scaleVal = 1.15
        stats[4] -= 1 #Increases speed and ensures that it is at a max of 1
        if stats[4] < 1:
            stats[4] = 1

    for i in range(len(stats)): #Updates all stats except speed
        if i != 4:
            stats[i] = int(stats[i]*scaleVal)
    
    return stats

def Get_Enemy(difficulty):
    '''
    Creates a character record for an enemy and scales stats based on difficulty
    '''
    specieName = Get_Species()[0] #Gets random specie name
    attackOptions = Get_Attacks(specieName) #Gets list of attack possibilities
    attacks = []
    for i in range(len(attackOptions)): #Gets a list of attacks for the enemy
        attacks.append(Attacks[attackOptions[i][0]])
    ability = Abilities[Get_Abilities(specieName)[0]] #Gets a random ability for the enemy
    enemy = Make_Character(specieName,specieName,attacks,ability)

    if difficulty != 2:
        enemy.stats = Scale_Enemy(enemy.stats,difficulty)

    return enemy
    
def Player_Move_Select(attacks):
    '''
    Displays attack options to the user and gets which move to use
    Takes attack options as input and returns a single move
    '''
    attackNames = []
    for i in range(len(attacks)): #Creates a list of names for user selection
        attackNames.append(attacks[i].name)
    attackIndex = Display_Options("What attack do you want to use? ",attackNames)-1
    attack = attacks[attackIndex]
    return attack

def Enemy_Move_Select(attacks):
    '''
    Gets a random attack for the enemy to use
    Takes attack options as input and returns a single move
    Currently chances are:
        Damage        - 35%
        Status        - 20%
        Damage/status - 30%
        DoT           - 15%
    '''
    n = randint(1,100) #Randomly selects a move to use
    if n <= 35:
        attack = attacks[0]
    elif n > 35 and n <= 55:
        attack = attacks[1]
    elif n > 55 and n <= 85:
        attack = attacks[2]
    else:
        attack = attacks[3]
    return attack

def Deal_Damage(attacker,defender,move):
    '''
    Deals damage to the defender based off of attacker, defender and move's stats
    Takes attacker, defender and move as inputs
    Returns updated defender stats as outputs
    '''
    if defender.ability.ID != 15 and (move.element != 1 or move.element != 2): #If the defending character has an ability that modifies type bonus
        typeBonus = elementEffective[move.element][defender.type1] * elementEffective[move.element][defender.type2] #Gets overall type bonus
    else:
        typeBonus = 1
        
    attackRand = randint(75,100)/100 #Gets random number to multiply damage by

    ablMultiplier = Apply_DM_Ability(attacker,defender,move)

    power = int(((move.power * attacker.stats[2])/(10 * defender.stats[3])) * typeBonus * attackRand * ablMultiplier) #Calculates damage
    if power < 1:
        power = 1
    defender.stats[0] -= power
    if defender.stats[0] < 0:
        defender.stats[0] = 0

    if typeBonus != 0: #Printing out correct battle text
        print("It did %s damage!" %(power))
        if typeBonus > 1:
            print("Its super-effective!")
        elif typeBonus < 1:
            print("Its not very effective...")
    else:
        print("But it had no effect...")

    return(defender)

def Deal_Status(attacker,defender,move):
    '''
    Affects stats of attacker or defender depending on the move's stats
    Takes attacker, defender and move as inputs
    Returns updated attack and defender as outputs
    '''

    attackType = move.status
    
    if attackType == 1 or attackType == 2: #Determines how much to change the power
        change = move.power
    else:
        change = move.secondaryStat
        
    if attackType == 1 or attackType == 3: #Changes stat
        attacker.stats[move.statChange] += change
    else:
        defender.stats[move.statChange] -= change

    if attacker.stats[0] >= attacker.stats[1]: #Corrects health stat of attacker
        attacker.stats[0] = attacker.stats[1]
    elif attacker.stats[0] < 0:
        attacker.stats[0] = 0

    for i in range(len(attacker.stats)-1): #Makes sure that no stat (other than health) is < 1
        if attacker.stats[i+1] < 1:
            attacker.stats[i+1] = 1
        if defender.stats[i+1] < 1:
            defender.stats[i+1] = 1

    if attackType == 1 or attackType == 3: #Defines keywords for printing
        name = attacker.name
        if move.secondaryStat >= 0:
            quality = 'increased'
            quantity = str(change)
        else:
            quality = 'decreased'
            quantity = str(-1*change)
    else:
        name = defender.name
        quality = 'decreased'
        quantity = str(change)

    if move.statChange == 0: #If the move increases/decreases attacker's health (special printing case)
        if move.secondaryStat < 0:
            print("%s was hit by recoil!" %(name))
            print("%s lost %s health!" %(name,quantity))
        else:
            print("%s healed for %s health!" %(name,quantity))
            
    elif move.statChange == 2:
        stat = 'attack'
    elif move.statChange == 3:
        stat = 'defence'
    elif move.statChange == 4:
        stat = 'speed'
    else:
        stat = 'accuracy'

    if move.statChange != 0:
        print("%s's %s %s by %s" %(name,stat,quality,quantity))
        
    return(attacker,defender)

def Deal_DoT(defender,move):
    '''
    Sets up DoT damage (doesn't actually affect health) for next turn
    Takes defender and move as inputs
    Returns updated defender
    '''
    duration = randint(3,5)
    power = round(((move.power/100 + 0.1)/duration)*defender.stats[1])
    if power < 1:
        power = 1
    defender.DoT = [power,duration]
    print("%s was affected by %s!" %(defender.name,move.name))
    return defender

def Move_Execute(attacker,defender,move):
    '''
    Carries out an attack, 'move' executed by 'attacker' that targets 'defender'
    Takes attacker, defender and move stats as input
    Updates attacker and defender stats and returns as output
    '''

    Display_ASCII(attacker.species,defender.species,move.displayType)
    print("%s used %s!" %(attacker.name,move.name))

    move = Apply_CM_Ability(attacker,move)

    attackType = move.status
    skipVal = Apply_AS_Ability(defender,attackType)

    accuracyChance = randint(1,100) #Determines whether the attack hits or not
    if accuracyChance <= (((move.accuracy + attacker.stats[5])/2)+10):
        accuracy = True
    else:
        accuracy = False
        print("But it missed!")
    
    if (attackType == 0 or attackType == 3 or attackType == 4) and accuracy and skipVal != 1: #If the attack deals damage
        defender = Deal_Damage(attacker,defender,move)

    if (attackType == 1 or attackType == 2 or attackType == 3 or attackType == 4) and accuracy and skipVal != 2: #If the attack affects another statistic
        attacker,defender = Deal_Status(attacker,defender,move)

    if attackType == 5 and accuracy and skipVal != 3: #If the attack is DoT
        defender = Deal_DoT(defender,move)

    if accuracy:
        attacker = Apply_AA_Ability(defender,attacker,attackType)

    return(attacker,defender)
            

def Player_Move(save,enemy):
    '''
    Carries out a player's turn by getting and executing a move
    Takes player save and enemy data as input, updates and returns as output
    '''
    move = Player_Move_Select(save.character.attacks)
    save.character,enemy = Move_Execute(save.character,enemy,move)
    return(save,enemy)

def Enemy_Move(save,enemy):
    '''
    Carries out the enemy's turn by getting and executing a move
    Takes player save and enemy data as input, updates and returns as output
    '''
    move = Enemy_Move_Select(enemy.attacks)
    enemy,save.character = Move_Execute(enemy,save.character,move)
    return(save,enemy)

def DoT(save,enemy):
    '''
    Calculates damage over time determined by player and enemy stats
    Takes player save and enemy stats as input and returns updated as output
    '''
    if save.character.DoT[1] != 0: #If the player takes DoT damage
        save.character.stats[0] -= save.character.DoT[0]
        save.character.DoT[1] -= 1
        print("%s took %s DoT damage!\n" %(save.character.name,save.character.DoT[0]))
        if save.character.stats[0] < 0:
            save.character.stats[0] = 0
    
    if enemy.DoT[1] != 0: #If the enemy takes DoT damage
        enemy.stats[0] -= enemy.DoT[0]
        enemy.DoT[1] -= 1
        print("%s took %s DoT damage!\n" %(enemy.name,enemy.DoT[0]))
        if enemy.stats[0] < 0:
            enemy.stats[0] = 0

    return(save,enemy)

def Execute_Turn(save,enemy,turn):
    '''
    Executes a single turn of combat and updates player and enemy stats
    Takes player save, enemy stats and turn number as inputs
    Returns player save and enemy stats as output
    '''
    print("\n#----------NEW ROUND-----------#")
    playerTurnVal = Apply_Turn_Ability(save.character)
    enemyTurnVal = Apply_Turn_Ability(enemy)

    if playerTurnVal == -1 and enemyTurnVal == 1: #If the enemy prevents movement and the player forces movement and vice versa
        enemyTurnVal == 0
    if enemyTurnVal == -1 and playerTurnVal == 1:
        playerTurnVal == 0
    
    if (turn % save.character.stats[4] == 0 or playerTurnVal == 1) and enemyTurnVal != -1: #If the player can attack
        save,enemy = Player_Move(save,enemy)
        print('')
    else:
        print("%s is getting ready to attack!\n" %(save.character.name))

    if save.character.stats[0] <= 0 or enemy.stats[0] <= 0:
        return(save,enemy)
    
    if (turn % enemy.stats[4] == 0 or enemyTurnVal == 1) and playerTurnVal != -1: #If the enemy can attack
        save,enemy = Enemy_Move(save,enemy)
        print('')
    else:
        print("%s is getting ready to attack!\n" %(enemy.name))
    save,enemy = DoT(save,enemy) #Executing DoT damage

    return(save,enemy)

def Battle(save):
    '''
    Engages the user in battle with a selected enemy and resolves encounter
    Takes a save record as input and returns an updated save file as output
    '''
    enemy = Get_Enemy(save.difficulty) #Gets enemy
    print("\n#----------NEW BATTLE----------#") #Displays initial battle text
    print("A wild %s appeared!" %(enemy.name))

    oldStats = save.character.stats.copy() #Creates a list of the original stats before entering battle

    save.character,enemy = Apply_BoB_Ability(save.character,enemy)
    enemy,save.character = Apply_BoB_Ability(enemy,save.character)

    turn = 1 #Sets turn counter to 1 initially
    while save.character.stats[0] > 0 and enemy.stats[0] > 0 and turn < 50: #Main battle loop
        save,enemy = Execute_Turn(save,enemy,turn)
        
        save.character,enemy = Apply_EoT_Ability(save.character,enemy) #Applies end of turn (EoT) abilities for enemy and player
        enemy,save.character = Apply_EoT_Ability(enemy,save.character)

        print("%s: %s/%s" %(save.character.name,save.character.stats[0],save.character.stats[1]))
        print("%s: %s/%s" %(enemy.name,enemy.stats[0],enemy.stats[1]))

        turn += 1
        temp = input("\nPress Enter to continue...")        

    if save.character.stats[0] <= 0: #Checks who won the game
        save.gameOver -= 1 #You lose a life if you lose the battle
        print("The terrifying %s crushes you with a smirk." %(enemy.name))
    elif enemy.stats[0] <= 0:
        print("You successfully defeated the funny-looking %s!" %(enemy.name))
        save.inventory = Get_Item(save)
    else:
        print("You ran away like a coward.")

    save.character.stats[1:] = oldStats[1:]#Replaces old stats except current health with original stats
    save.character.DoT = [0,0]
    
    return save
