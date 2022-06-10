#Created by Justin Stewart
#Github: NotBlasto
#Program: Text-Based-DS3
# This program This project is a reimagination of Dark Souls 3 as a choose your own adventure game. 
# I chose to create this project as a massive fan of the series and programmer seeking practice. 
# My hope is to provide fans of the series with a new way to experience one of their favorite storylines, while still maintaining all of the core action combat elements players have come to know and love throughout the series. 
# The game currently only allows players access up to the High Wall of Lothric, but has provided a framework for expansion throughout all zones. Combat options include: attack, heavy attack, roll, and estus flask. 
# Boss behavior is designed to mimic the original, with multiple phases and increasingly varying attack patterns. 
# I do not claim any right to the names and world of Dark Souls 3 owned by FromSoftware utilized in this project. 
# If there are any questions or concerns about the usage of any elements in this project, send me a message and I will respond promptly.


#Necessary Imports
import random
import sys
import pygame
from pygame import mixer
import json
from dataclasses import dataclass
from os.path import exists
from time import sleep

#LIST OF NOTES / IDEAS THAT ARE IN THE WORKS:
#Finish ability descriptions and dialogue.
#Work on Intro sequence.
#Need to fix what happens if player searches. Right now it just loops back to firelink.
#Maybe make it so that player choices are saved to a new file.
#Work on bonfire problem, currently bonfires do not utilize the Bonfire class. Should be if the user chooses that location and that bonfire value = 1, they can go. 
#(Cont)However, I want it to be that they dont appear in the list of available bonfires unless lit. 
#Make it so hollows respawn and all elite enemies do not.
#May need to make souls drop. Current idea is to make it in the you died function, where upon death, the soul amount is appended to a new list. 
#(Cont)And upon going back, can be restored.
#May have to think about soul farming 
#Code Gundyr fight to have the sword inside of him, provide enough extra health for 2 hits.
#Check Zones to see how spawn/despawn is working and apply to all other soul events if needed. 
#Keep track of which bonfires are available to the player and when.

@dataclass
class Enemy:
    enemyhealth: int
    enemyoptions: int
    enemychoice: int
    enemyattacks: int
    enemyneutral: int
    neutralchoice: int
    playerchoice: int
    playerstamina: int
@dataclass
class Bonfire:
    CemetaryOfAsh = 0
    FirelinkShrine = 0
    HighWallOfLothric = 0

#Class dedicated to storing player's one-time choices so that they cannot be repeated and exploited.
@dataclass
class Playerchoices:
    CemetaryLeft = 0
    CemetaryRight = 0
    Room1_Searched = 0
    Lothric_Bonfire_Item = 0

#Class storing all functions for non-boss combat encounters.
@dataclass
class Mobs:
    #may need to track each death individually, otherwise players can kill other mobs and this wont spawn, or all mobs are farmable and don't care.
    #DeadRavenousCrystalLizard: 0
    def RavenousCrystalLizard():
        Enemy.enemyhealth = 5
        Enemy.playerstamina = GameState.maxstamina
        Enemy.enemyoptions = [1,2]
        Enemy.enemyneutral = [1,2] 
        while Enemy.enemyhealth !=0:
                Enemy.enemyattacks = [1,2,3]
                Enemy.enemyattackchoice = random.choice(Enemy.enemyattacks)
                Enemy.enemychoice = random.choice(Enemy.enemyoptions)
                Enemy.neutralchoice = random.choice(Enemy.enemyneutral)
                Enemy.playerchoice = input('Would you like to light attack, heavy attack, roll, or estus? 1, 2, 3, or 4: ')
                if Enemy.playerchoice == '1' and Enemy.playerstamina <= 0:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '1' and Enemy.playerstamina >= 1:
                    if Enemy.playerchoice == '1' and Enemy.enemychoice == 1 :
                        lightattack()
                        if Enemy.enemyattackchoice == 1:
                            print('Ravenous Crystal Lizard does thing 1') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 2:
                            print('Ravenous Crystal Lizard does thing 2')
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 3:
                            print('Ravenous Crystal Lizard does thing 3') 
                            deincrementhealth()
                    if Enemy.playerchoice == '1' and Enemy.enemychoice == 2:
                        lightattack()
                        if Enemy.neutralchoice == 1:
                            print('You Hit The Enemy With Light Attack')
                            deincrementenemyhealth()
                        if Enemy.neutralchoice == 2:
                            print('Ravenous Crystal Lizard Dodged Your Attack')
                if Enemy.playerchoice == '2' and Enemy.playerstamina < 3:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '2' and Enemy.playerstamina >= 3:
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 1 :
                        heavyattack()
                        if Enemy.enemyattackchoice == 1:
                            print('Ravenous Crystal Lizard does thing 1') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 2:
                            print('Ravenous Crystal Lizard does thing 2')
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 3:
                            print('Ravenous Crystal Lizard does thing 3') 
                            deincrementhealth()
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 2:
                        heavyattack()                    
                        if Enemy.neutralchoice == 1:
                            print('You Hit The Enemy With Heavy Attack')
                            heavyattackdamage()
                        if Enemy.neutralchoice == 2:
                            print('Ravenous Crystal Lizard Dodged Your Attack')              
                if Enemy.playerchoice == '3' and Enemy.playerstamina < 4:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '3' and Enemy.playerstamina >= 4:
                    if Enemy.playerchoice == '3' and Enemy.enemychoice == 1:
                        roll()
                        if Enemy.enemyattackchoice == 1:
                            print('You dodge thing 1') 
                        if Enemy.enemyattackchoice == 2:
                            print('You dodge thing 2')
                        if Enemy.enemyattackchoice == 3:
                            print('You dodge thing 3')                 
                    if Enemy.playerchoice== '3' and Enemy.enemychoice == 2:
                        roll()
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 1:
                    if Enemy.enemyattackchoice == 1:
                        estus()
                        print('Ravenous Crystal Lizard 1') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 2:
                        estus()
                        print('Ravenous Crystal Lizard 2')
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 3:
                        estus()
                        print('Ravenous Crystal Lizard 3') 
                        deincrementhealth()
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 2:
                    estus()
        if Enemy.enemyhealth == 0:
            print('You defeated the Ravenous Crystal Lizard. You are awarded 1 soul and 1 titanite')
            givesouls()
            giveTitanite()
                                 
#Class storing all functions for boss encounters. May consolidate Mob and Boss classes.   
@dataclass
class Bosses:
    def Gundyr():
        Enemy.enemyhealth = 10
        Enemy.playerstamina = GameState.maxstamina
        Enemy.enemyoptions = [1,2]
        Enemy.enemyneutral = [1,2] 
        while Enemy.enemyhealth !=0:
            if Enemy.enemyhealth >=6:
                Enemy.enemyattacks = [1,2,3]
                Enemy.enemyattackchoice = random.choice(Enemy.enemyattacks)
                Enemy.enemychoice = random.choice(Enemy.enemyoptions)
                Enemy.neutralchoice = random.choice(Enemy.enemyneutral)
                Enemy.playerchoice = input('Would you like to light attack, heavy attack, roll, or estus? 1, 2, 3, or 4: ')
                if Enemy.playerchoice == '1' and Enemy.playerstamina <= 0:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '1' and Enemy.playerstamina >= 1:
                    if Enemy.playerchoice == '1' and Enemy.enemychoice == 1 :
                        lightattack()
                        if Enemy.enemyattackchoice == 1:
                            print('Iudex Gundyr does thing 1') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 2:
                            print('Iudex Gundyr does thing 2')
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 3:
                            print('Iudex Gundyr does thing 3') 
                            deincrementhealth()
                    if Enemy.playerchoice == '1' and Enemy.enemychoice == 2:
                        lightattack()
                        if Enemy.neutralchoice == 1:
                            print('You Hit The Enemy With Light Attack')
                            deincrementenemyhealth()
                        if Enemy.neutralchoice == 2:
                            print('Iudex Gundyr Dodged Your Attack')
                if Enemy.playerchoice == '2' and Enemy.playerstamina < 3:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '2' and Enemy.playerstamina >= 3:
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 1 :
                        heavyattack()
                        if Enemy.enemyattackchoice == 1:
                            print('Iudex Gundyr does thing 1') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 2:
                            print('Iudex Gundyr does thing 2')
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 3:
                            print('Iudex Gundyr does thing 3') 
                            deincrementhealth()
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 2:
                        heavyattack()                    
                        if Enemy.neutralchoice == 1:
                            print('You Hit The Enemy With Heavy Attack')
                            heavyattackdamage()
                        if Enemy.neutralchoice == 2:
                            print('Iudex Gundyr Dodged Your Attack')              
                if Enemy.playerchoice == '3' and Enemy.playerstamina < 4:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '3' and Enemy.playerstamina >= 4:
                    if Enemy.playerchoice == '3' and Enemy.enemychoice == 1:
                        roll()
                        if Enemy.enemyattackchoice == 1:
                            print('You dodge thing 1') 
                        if Enemy.enemyattackchoice == 2:
                            print('You dodge thing 2')
                        if Enemy.enemyattackchoice == 3:
                            print('You dodge thing 3')                 
                    if Enemy.playerchoice== '3' and Enemy.enemychoice == 2:
                        roll()
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 1:
                    if Enemy.enemyattackchoice == 1:
                        estus()
                        print('Iudex Gundyr does thing 1') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 2:
                        estus()
                        print('Iudex Gundyr does thing 2')
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 3:
                        estus()
                        print('Iudex Gundyr does thing 3') 
                        deincrementhealth()
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 2:
                    estus()
            if Enemy.enemyhealth <= 5:
                print('Gundyr Transforms into Pus of Man')
                break
        while Enemy.enemyhealth !=0:
                Enemy.enemyattacks = [1,2,3,4]
                Enemy.enemyattackchoice = random.choice(Enemy.enemyattacks)
                Enemy.enemychoice = random.choice(Enemy.enemyoptions)
                Enemy.neutralchoice = random.choice(Enemy.enemyneutral)
                Enemy.playerchoice = input('Would you like to light attack, heavy attack, roll, or estus? 1, 2, 3, or 4: ')
                if Enemy.playerchoice == '1' and Enemy.playerstamina <= 0:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '1' and Enemy.playerstamina >= 1:
                    if Enemy.playerchoice == '1' and Enemy.enemychoice == 1:
                        lightattack()
                    if Enemy.enemyattackchoice == 1:
                        print('Iudex Gundyr does thing 1') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 2:
                        print('Iudex Gundyr does thing 2')
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 3:
                        print('Iudex Gundyr does thing 3') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 4:
                        print('Iudex Gundyr Hits You With Slam And Devour')
                        bossdamage()                
                if Enemy.playerchoice == '1' and Enemy.enemychoice == 2:
                    lightattack()
                    if Enemy.neutralchoice == 1:
                        deincrementenemyhealth()
                        print('You Hit The Enemy With Light Attack')
                    if Enemy.neutralchoice == 2:
                        print('Iudex Gundyr Dodged Your Attack')
                if Enemy.playerchoice == '2' and Enemy.playerstamina < 3:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '2' and Enemy.playerstamina >= 3:
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 1 :
                        heavyattack()
                        if Enemy.enemyattackchoice == 1:
                            print('Iudex Gundyr does thing 1') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 2:
                            print('Iudex Gundyr does thing 2')
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 3:
                            print('Iudex Gundyr does thing 3') 
                            deincrementhealth()
                        if Enemy.enemyattackchoice == 4:
                            print('Iudex Gundyr Hits You With Slam And Devour')
                            bossdamage()
                    if Enemy.playerchoice == '2' and Enemy.enemychoice == 2:
                        heavyattack()
                        if Enemy.neutralchoice == 1:
                            heavyattackdamage()
                            print('You Hit The Enemy With Heavy Attack')
                        if Enemy.neutralchoice == 2:
                            print('Iudex Gundyr Dodged Your Attack')              
                if Enemy.playerchoice == '3' and Enemy.playerstamina < 4:
                    print ('Not enough stamina')
                if Enemy.playerchoice == '3' and Enemy.playerstamina >= 4:
                    if Enemy.playerchoice == '3' and Enemy.enemychoice == 1 :
                        roll()
                        if Enemy.enemyattackchoice == 1:
                            print('You dodge thing 1') 
                        if Enemy.enemyattackchoice == 2:
                            print('You dodge thing 2')
                        if Enemy.enemyattackchoice == 3:
                            print('You dodge thing 3')                 
                    if Enemy.playerchoice== '3' and Enemy.enemychoice == 2:
                        roll()
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 1:
                    if Enemy.enemyattackchoice == 1:
                        estus()
                        print('Iudex Gundyr does thing 1') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 2:
                        estus()
                        print('Iudex Gundyr does thing 2')
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 3:
                        estus()
                        print('Iudex Gundyr does thing 3') 
                        deincrementhealth()
                    if Enemy.enemyattackchoice == 4:
                        print('Iudex Gundyr Hits You With Slam And Devour')
                        bossdamage()                
                if Enemy.playerchoice == '4' and Enemy.enemychoice == 2:
                    estus()
        if Enemy.enemyhealth == 0:
            print('HEIR OF FIRE DESTROYED')
            givebossSouls()
            answer = input('The great champion dissipates into nothing but ash, use firelink greatsword to link the bonfire? yes/no: ')
            if answer.lower().strip() == 'yes':
                Bonfire.CemetaryOfAsh = 1
                GameState.deadbosses += 1
                GundyrBonfire()
            else:
                answer = input('Are you sure you dont want to light the bonfire? You will not restore health, estus, or respawn here. yes/no')
                if answer.lower().strip() == 'yes':
                    print('You refuse to light the bonfire')
                    GameState.deadbosses += 1
                    GameState.playerZone = 0
                    GameState.playerLevel = 0
                elif answer.lower().strip() == 'no':
                    answer = input('The great champion dissipates into nothing but ash, use firelink greatsword to link the bonfire? yes/no: ')
                    if answer.lower().strip() == 'yes':
                        GundyrBonfire()
                        GameState.deadbosses += 1
                        print('You continue on from where the great champion has fallen and discover a land filled with smokey air. A beautiful, yet dilipidated shrine is before you.')
                                    
#Class storing functions for every zone to be ran upon players making a given choice. 
@dataclass
class Zones:
    def Zones():
        if GameState.playerZone == 0 and GameState.playerLevel == 0:
                print('----------CEMETARY OF ASH----------')
                answer = input('You Spawn in to Cemetary of Ash, you see three paths before you, go straight, left, or right? ')
                if answer.lower().strip() == 'right':
                    GameState.playerZone = 0
                    GameState.playerLevel = 1
                    while GameState.playerZone == 0 and GameState.playerLevel == 1:
                        if Playerchoices.CemetaryRight == 0:
                            print('You encounter a Ravenous Crystal Lizard, prepare for combat')
                            Mobs.RavenousCrystalLizard()
                            Playerchoices.CemetaryRight+=1
                            GameState.playerZone = 0
                            GameState.playerLevel = 0
                            save()
                    else: print('Ravenous Crystal Lizard Already Slain')
                elif answer.lower().strip() == 'left':
                    GameState.playerZone = 0
                    GameState.playerLevel = 2
                    while GameState.playerZone == 0 and GameState.playerLevel == 2:
                        if Playerchoices.CemetaryLeft == 0:
                            givesouls()
                            print('You found a soul! You now have', GameState.souls, 'souls')
                            Playerchoices.CemetaryLeft+=1
                            print('You head back to the main path...')
                            GameState.playerZone = 0
                            GameState.playerLevel = 0
                            save()
                    else: print('Already claimed soul')
                elif answer.lower().strip() == 'straight':
                    GameState.playerZone = 0
                    GameState.playerLevel = 3
                    if GameState.deadbosses == 0:
                        answer = input('You see a fog gate go through? yes/no: ')
                        if answer.lower().strip() == 'yes':
                            print('------------IUDEX GUNDYR-----------')
                            Bosses.Gundyr()
                            print('You continue on from where the great champion has fallen and discover a land filled with smokey air. A beautiful, yet dilipidated shrine is before you.')
                            GameState.playerZone = 1
                            GameState.playerLevel = 0
                    else:
                        answer = input('Progress to Firelink Shrine? Y / N: ')
                        if answer.lower().strip() == 'y':
                            print('You continue on from where the great champion has fallen and discover a land filled with smokey air. A beautiful, yet dilipidated shrine is before you.')
                            GameState.playerZone = 1
                            GameState.playerLevel = 0
                        else:
                            GameState.playerZone = 0
                            GameState.playerLevel = 0


        if GameState.playerZone == 1 and GameState.playerLevel == 0:
                print('----------FIRELINK SHRINE----------')
                print('Within Firelink Shrine you see three unfamiliar faces before you. Speak to: , firekeeper, blacksmith, continue')
                answer = input('Would you like to: Visit the Firekeeper, Visit the Blacksmith, or Continue to High Wall of Lothric? 1, 2, 3: ')
                if answer.lower().strip() == '1':
                    print('You see a woman who introduces herself as the firekeeper. She can take what souls you have and grant you levels.')
                    answer = input('Would you like to spend souls to level up? Each level costs 5 souls. Yes / No: ')
                    if answer.lower().strip() == 'yes':
                        if GameState.souls < 5:
                            print('not enough souls to level up')
                        if GameState.souls >=5:
                            GameState.souls=GameState.souls-5
                            GameState.level = GameState.level+1
                            print('You spend 5 souls to level up. You are now level:',GameState.level, 'You now have',GameState.souls, 'souls remaining')
                            if GameState.level+1:      
                                GameState.maxhealth=GameState.maxhealth+1
                                GameState.maxstamina=GameState.maxstamina+2
                                print('You now have', GameState.maxhealth,'maximum health and', GameState.maxstamina, 'maximum stamina')
                                
                    if answer.lower().strip() == 'no':
                            print('return to other options will be here')
                elif answer.lower().strip() == '2':
                    answer = input('You see a man hammering away at an anvil. He can upgrade your weapon and estus flask, Upgrade weapon or estus? 1 or 2: ')
                    if answer.lower().strip() == '1':
                        if GameState.titanite < 1:
                            print('Not enough titanite')
                        if GameState.titanite >=1:
                            GameState.weaponlevel = GameState.weaponlevel+1
                            print('Weapon Upgraded to +'+(str(GameState.weaponlevel)))
                    if answer.lower().strip() == '2':
                        if GameState.estusShard < 1:
                            print('You do not have any estus shards')
                        if GameState.estusShard >=1:
                            GameState.estusShard = GameState.estusShard-1
                            GameState.maxestus = GameState.maxestus+1
                            print('Estus Flask Upgraded. Your Estus Flask now has',(str(GameState.maxestus)),'charges')
                elif answer.lower().strip() == '3':
                    GameState.playerZone = 2
                    GameState.playerLevel = 0
                    Zones.Zones()
        if GameState.playerZone == 2 and GameState.playerLevel == 0:
                    BeamEncounter = [1,2]
                    print ('You spawn at High Wall of Lothric')
                    print ('Before you lies a staircase leading downwards. Upon descending the staircase, two paths lie before you.')
                    answer = input('Would you like to go right or left?')
                    if answer.lower().strip() == 'right':
                        print('An axe hollow spots you heading down the path')
                        print ('The axe hollow immediately sprints your way, leaping and coming down with an overhead attack, missing by a few feet.')
                        #instert combat scenario here
                        #if hollow defeated
                        #probably do delayed text timing
                    if answer.lower().strip() == 'left':
                        GameState.playerZone = 2
                        GameState.playerLevel = 1
                        while GameState.playerZone == 2 and GameState.playerLevel == 1:
                            print ('A single hollow holding a lantern spots you and clumsily lunges towards you')
                            #hollow combat scenario
                            #if hollow is defeated
                            print('You enter a dark, square room with a ladder that appears to descend to the floor below.')
                            answer = input('Descend the ladder, or search the area?' '"Ladder" or "Search"')
                            if answer.lower().strip() == "search" and Playerchoices.Room1_Searched == 0:
                                print('You destroy the surrounding boxes in search of an item.')
                                givesouls()
                                Playerchoices.Room1_Searched +=1
                            elif answer.lower().strip() == "search" and Playerchoices.Room1_Searched > 0:
                                print ('Room has already been searched')
                                print ('Taking you back...')
                                GameState.playerZone = 2
                                GameState.playerLevel = 1
                            if answer.lower().strip() == "ladder":
                                print('You descend the ladder to reveal a dark hallway.')
                                print('You progress down the hallway and through a doorway on your left')
                                print('You hear a distant screech...')
                                print('Before you lies a staircase leading upwards, and a path adjacent leading straight')
                                print('What is up the staircase cannot be seen')
                                print('The path leading straight is filled with numerous hollows')
                                print ('You hear wings flap in the distance...')
                                answer = input('Would you like to go up the stairs or proceed straight "Stairs" or "Straight"')
                                if answer.lower().strip() == "stairs":
                                    print ('A dragon flies above, pouring flame breath where you stand')
                                    #I don't think player dies here, would like to get mimic fight in
                                if answer.lower().strip() == 'straight':
                                    GameState.playerZone = 2
                                    GameState.playerLevel = 2
                                    while GameState.playerZone == 2 and GameState.playerLevel == 2:
                                        print ('A dragon flies above, landing on the pathway above.')
                                        print ('The dragon breathes fire upon the pathway above, and then the path before you, instantly killing the hollows.')
                                        print ('With the way clear, you proceed forward.')
                                        print ('An open door lies ahead.')
                                        print ('You hear the clanking of heavy footsteps...')
                                        print ('As you approach the end of the pathway, an unfamiliar armored knight wielding a sword and shield emerges from the darkness beyond the doorway.')
                                        print ('The knight begins sprinting your way with much more composure than previous enemies...')
                                        print ('Upon reaching you the knight shows no hesitation launching forward a lunging thrust, narrowly missing your body')
                                        #Combat for lothric knight
                                        #upon winning combat
                                        print ('You enter the doorway beyond the fallen knight to reveal a dilapidated room')
                                        print ('Upon entering the dilapidated room you see a narrow beam outstretched with an item straight ahead, a doorway to your right, and hear multiple enemies below')
                                        #chance to fall off beam
                                        answer = input('Try to walk across the beam to get the item? Or go through the doorway to the right? "straight" or "right')
                                        if answer.lower().strip() == 'straight':
                                            BeamOutcome = random.choice(BeamEncounter)
                                            if BeamOutcome == 1:
                                                #Maybe give item here as well, souls placeholder for now
                                                givesouls()
                                            else:
                                                print('You reach for the item, losing your balance falling into the enemies below')
                                                #begin combat
                                            #CHANCE ENCOUNTER TO FALL INTO 3 ENEMIES, USE COLLECTIVE HP POOL FOR ALL OF THEM, AND AS HEALTH DECREASES ONE DIES ETC. EX 15HP FOR 3, AT 10, 1 DIES. 
                                            #ONLY INCREMENT THE ZONE ITEM IF THE PLAYER GETS THE ITEM SO THEY CAN COME BACK FOR IT IF THEY FALL
                                        if answer.lower().strip() == 'right':
                                            GameState.playerZone = 2
                                            GameState.playerLevel = 3
                                            while GameState.playerZone == 2 and GameState.playerLevel == 3:
                                                #save this game location
                                                print('You found a bonfire! There also appears to be an item glowing in the corner.')
                                                answer = input("Light the bonfire? Y/N")
                                                if answer.lower().strip == 'y':
                                                    Bonfire.HighWallOfLothric = 1
                                                    bonfire()
                                                    answer = input('Grab the item? Y/N')
                                                    if answer.lower().strip() == 'y' and Playerchoices.Lothric_Bonfire_Item == 0:
                                                        print ('You found a soul!')
                                                        givesouls()
                                                        Playerchoices.Lothric_Bonfire_Item = 1
                                                    elif answer.lower().strip() == 'y' and Playerchoices.Lothric_Bonfire_Item == 1:
                                                        print ('Item already obtained')
                                                    else:
                                                        answer = input('Go back down the stairs and proceed? Y/N ')
                                                        if answer.lower().strip() == 'y' and Playerchoices.Lothric_Bonfire_Item == 0:
                                                            print ('You proceed down the steps, sneaking behind the Lothric knight.' )
                                                            print ('You see an open doorway out to the right and the item still sitting on the beam.')
                                                            #add input
                                                        if answer.lower().strip() == 'y' and Playerchoices.Lothric_Bonfire_Item == 1:
                                                            print ('You proceed down the steps, sneaking behind the Lothric knight. You see an open doorway out to the right')
                                                            print ('You proceed outside, stepping into a rooftop overlook of the surrounding area. One path lies before you')
                                                            print('As you walk along the rooftop, you encounter a ladder down to another rooftop a few feet below.')
                                                            #maybe undo this input as there is no player choice, but need a trigger for the events
                                                            answer = input('Proceed down the ladder? Y/N')
                                                            if answer == 'y':
                                                                print ('As you descend the ladder you hear an unsettling noise...')
                                                                print ('A hollow erupts into a pus of man and charges your direction.')
                                                                #COMBAT FOR PUS OF MAN HOLLOW
                                                            




                                                else:
                                                    answer=input("Are you sure you don't want to light the bonfire? Y/N" )
                                                    if answer.lower().strip() == 'y':
                                                        print('You do not light the bonfire, game progress has not been saved, and estus has not been restored')
                                                    if answer.lower().strip() == 'n':
                                                        answer = input('Light the bonfire?' "Y/N")
                                                        if answer.lower().strip == 'y':
                                                            Bonfire.HighWallOfLothric
                                                            bonfire()
                                            
                                        
#Class tracking all important player character data.
@dataclass
class GameState:
    souls: int
    deadbosses: int
    estus: int
    health: int
    maxhealth: int
    maxstamina: int
    titanite: int
    estusShard: int
    maxestus: int
    level: int
    weapon: int
    weaponlevel: int
    playerZone: int
    playerLevel: int
#Class tracking all important enemy data.
@dataclass
class Enemy:
    enemyhealth: int
    enemyoptions: int
    enemychoice: int
    enemyattacks: int
    enemyneutral: int
    neutralchoice: int
    playerchoice: int
    playerstamina: int
#Function to save the game, ran at bonfires which function as checkpoints. 
def save():
    outfile = open("ds3.json", "w")
    outfile.write("souls:"+str(GameState.souls)+'\n'+"deadbosses:"+str(GameState.deadbosses)+'\n'+"maxhealth:"+str(GameState.maxhealth)+'\n'"maxstamina:"+str(GameState.maxstamina)+'\n'"titanite:"+str(GameState.titanite)+'\n'"estusShards:"+str(GameState.estusShard)+'\n'"maxestus:"+str(GameState.maxestus)+'\n'"level:"+str(GameState.level)+'\n'"weapon:"+str(GameState.weapon)+'\n'"weaponlevel:"+str(GameState.weaponlevel)+'\n'"CemetaryLeft:"+str(Playerchoices.CemetaryLeft)+'\n'"CemetaryRight:"+str(Playerchoices.CemetaryRight))
    outfile.close()    
    print('Game progress has been saved.')
#Estus flask / healing mechanic function called in combat scenarios. Can be upgraded throughout the game.
def estus():
    if GameState.health < GameState.maxhealth and GameState.estus !=0:
        GameState.health = min(GameState.health+1, GameState.maxhealth)
        GameState.estus = max(GameState.estus-1, 0)
        Enemy.playerstamina = min(Enemy.playerstamina+2, GameState.maxstamina)
        print('You heal 1 point of health. You have',GameState.health,'health left')
        print('You have',GameState.estus, 'estus flasks remaining')
        print('You regain stamina while you heal, you now have', Enemy.playerstamina,'stamina left')
    else:
        if GameState.health >= GameState.maxhealth:
            print('You are already full health and cannot heal')
        if GameState.estus == 0:
            print('You are out of estus flasks and cannot heal')
#Bonfire / save / teleport function
def GundyrBonfire():
    print('----------BONFIRE LIT----------')
    save()
    if GameState.estus < GameState.maxestus:
        GameState.estus = GameState.maxestus
    if GameState.health < GameState.maxhealth:
        GameState.health = GameState.maxhealth

def bonfire():
    print('----------BONFIRE LIT----------')
    #outfile = open("ds3.json", "w")
    #outfile.write("Souls:"+str(GameState.souls)+'\n'+"Deadbosses:"+str(GameState.deadbosses)+'\n'+"MaxHealth:"+str(GameState.maxhealth)+'\n'"MaxStamina:"+str(GameState.maxstamina)+'\n'"Titanite:"+str(GameState.titanite)+'\n'"EstusShards:"+str(GameState.estusShard)+'\n'"MaxEstus:"+str(GameState.maxestus)+'\n'"Level:"+str(GameState.level)+'\n'"Weapon:"+str(GameState.weapon)+'\n'"WeaponLevel:"+str(GameState.weaponlevel)+'\n'"CemetaryLeft:"+str(Playerchoices.CemetaryLeft)+'\n'"CemetaryRight:"+str(Playerchoices.CemetaryRight))
    #outfile.close()    
    save()
    if GameState.estus < GameState.maxestus:
        GameState.estus = GameState.maxestus
    if GameState.health < GameState.maxhealth:
        GameState.health = GameState.maxhealth
    answer=input('Would you like to travel? 1 / 2: ')
    if answer.lower().strip() == '1':
        print('Where would you like to go?')
        answer = input("1.Cemetary Of Ash"+'\n'+"2.Firelink Shrine"+'\n'+"3.High Wall Of Lothric"+'\n'+"Enter Selection:")
        if answer == '1' and Bonfire.CemetaryOfAsh == 1:
            GameState.playerZone = 0
            GameState.playerLevel = 0
            Zones.Zones()
        if answer == '2' and Bonfire.FirelinkShrine == 1:
            GameState.playerZone = 1
            GameState.playerLevel = 0
            Zones.Zones()
        
        if answer == '3':
            GameState.playerZone = 2
            GameState.playerLevel = 0
        else:
            print('Cannot teleport there yet')
            GameState.playerZone = GameState.playerZone
            GameState.playerLevel = 0
            Zones.Zones()
    else:
        GameState.playerZone = GameState.playerZone
        GameState.playerLevel = 0
        Zones.Zones()
#Function to give player titanite (Upgrade material), may just reward upon winning certain combats and searching certain areas.
def giveTitanite():
    GameState.titanite = GameState.titanite+1
    print('You now have:',GameState.titanite, 'titanite')    
#Function to open save, ran at start of game.    
def opensave():
    array = []
    filename = "ds3.json"
    file = open(filename,"r")
    lines = file.readlines()
    for line in lines:
        templine = line.split(':')
        array.append(templine[1])
    GameState.souls = int(array[0])
    GameState.deadbosses = int(array[1])
    GameState.maxhealth = int(array[2])
    GameState.maxstamina = int(array[3])
    GameState.titanite = int(array[4])
    GameState.estusShard = int(array[5])
    GameState.maxestus = int(array[6])
    GameState.level = int(array[7])
    GameState.weapon = int(array[8])
    GameState.weaponlevel = int(array[9])
    Zones.CemetaryLeft = int(array[10])
    Zones.CemetaryRight = int(array[11])
    
    file.close()
#Function to give boss souls / greater amount of souls / may also do away with this function and simply reward upon winning combat.
def givebossSouls():
    GameState.souls = GameState.souls+3
    print('You now have:',GameState.souls, 'souls')
#Function when player takes damage.
def deincrementhealth():
    GameState.health = min(GameState.health - 1, GameState.health)
    print('You have', GameState.health, 'health left')
    if GameState.health <= 0:
        print ('YOU DIED')
        sys.exit(0)
#Function to takes significant boss damage. 
def bossdamage():
    GameState.health = max(GameState.health - 2, 0)
    print('You have', GameState.health, 'health left')
    if GameState.health <= 0:
        print('YOU DIED') 
#Function for player light attack.
def lightattack():
    if GameState.weapon == 1:
        Enemy.playerstamina = max(Enemy.playerstamina - 1, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 2, 10)
        print('You attempt to light attack the target, you now have', Enemy.playerstamina,'stamina left')
    if GameState.weapon == 2:
        Enemy.playerstamina = max(Enemy.playerstamina - 2, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 3, 10)
        print('You attempt to light attack the target, you now have', Enemy.playerstamina,'stamina left')
    if GameState.weapon == 3: 
        Enemy.playerstamina = max(Enemy.playerstamina - 3, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 4, 10)
        print('You attempt to light attack the target, you now have', Enemy.playerstamina,'stamina left')
#Function for player heavy attack.
def heavyattack():
    if GameState.weapon == 1:
        Enemy.playerstamina = max(Enemy.playerstamina - 3, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 2, 10)
        print('You attempt to heavy attack the target, you now have', Enemy.playerstamina,'stamina left')
    if GameState.weapon == 2:
        Enemy.playerstamina = max(Enemy.playerstamina - 4, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 2, 10)
        print('You attempt to heavy attack the target, you now have', Enemy.playerstamina,'stamina left')
    if GameState.weapon == 3: 
        Enemy.playerstamina = max(Enemy.playerstamina - 5, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 2, 10) 
        print('You attempt to heavy attack the target, you now have', Enemy.playerstamina,'stamina left')
#Function for player combat roll.
def roll():
        Enemy.playerstamina = max(Enemy.playerstamina - 4, 0)
        Enemy.playerstamina = min(Enemy.playerstamina + 2, 10)
        print('You roll, you now have', Enemy.playerstamina,'stamina left')                                    
#Function to decrease enemy health when hit.
def deincrementenemyhealth():
    if GameState.weapon == 1:
        damage = 1
        Enemy.enemyhealth = Enemy.enemyhealth-(damage+GameState.weaponlevel)
    if GameState.weapon == 2:
        damage = 2
        Enemy.enemyhealth = Enemy.enemyhealth-(damage+GameState.weaponlevel)
    if GameState.weapon == 3:
        damage = 3
        Enemy.enemyhealth = Enemy.enemyhealth-(damage+GameState.weaponlevel)
    #if Enemy.enemyhealth == 5:
        print ('------------IUDEX GUNDYR TRANSFORMS INTO PUS OF MAN------------')     
#Function for heavy attack damage
def heavyattackdamage():
    if GameState.weapon == 1:
        Enemy.enemyhealth = Enemy.enemyhealth-2
    if GameState.weapon == 2:
        Enemy.enemyhealth = Enemy.enemyhealth-4
    if GameState.weapon == 3:
        Enemy.enemyhealth = Enemy.enemyhealth-6
#Function to give player souls / like others may do away with this function and reward players upon looting.
def givesouls():
    GameState.souls = GameState.souls+1
    print('You now have:',GameState.souls, 'souls')
#Not implimented, Will play intro sequence of Dark Souls 3 for worldbuilding and immersion reasons.
def intro():
    print("Yes, indeed. It is called Lothric...")
#Start of game, load save, new save, weapon choice, while loop to keep game running continuously.
answer = input('load a save? or create a new character: 1 / 2: ')
if answer.lower().strip() == '1':
    file_exists = exists("ds3.json")
    if file_exists:
        opensave()
        print('save loaded')
    else:
        print('no save on file')
if answer.lower().strip() == '2':
    answer = int(input('Choose your weapon: Straight Sword, Greatsword, Ultra Greatsword. 1, 2, 3: '))
    if answer > 0 and answer <= 3:             
        GameState.weapon = answer
        GameState.deadbosses = 0
        GameState.health = 3
        GameState.souls = 0
        GameState.maxestus = 3
        GameState.estus = GameState.maxestus
        GameState.maxhealth = 3
        GameState.maxstamina = 10
        GameState.level = 1
        GameState.titanite = 0
        GameState.weaponlevel = 0
        GameState.estusShard = 0
        GameState.playerZone = 0
        GameState.playerLevel = 0
        print('Character created')
    else:
        print('Not a valid selection.')
while(1):
    Zones.Zones()