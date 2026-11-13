# importing random
import random
#Shared game information
pouch = []
creatures = ["Spiderling", "Scorned Spirit", "Cultist"]

#Set starting values
health = 100
gold = 20
hasKey = False
hasNote = False

#Defining the introduction
def introduction():
   
#Welcome the player
 print("=== ESCAPE THE CASTLE ===")
 print("Welcome, adventurer!")
#Get player name, age and character class
 playerName = input("Please state your name: ")
 playerAge = int(input("Please state your age: "))
 playerClass = input("What is your preferred class?: ")
 print() #empty line for spacing
 

#Display the character profile
 print("\n=== YOUR CHARACTER PROFILE ===")
 print(f"Name: {playerName}")
 print(f"Age: {playerAge}")
 print(f"Class: {playerClass}")
 print(f"Health: {health}")
 print(f"Gold: {gold}")
 print(f"Has Escape Key: {hasKey}")
 print() #empty line to separate text

#Begin the story
 print(f"You, {playerName}, wake up in a damp and dark cell.")
 print("The air is thick with the smell of mold and decay.")
 print("You can hear the distant sound of dripping water echoing through the stone corridors.")
 print("You have no memory of how you got here, but you know you must escape before whoever has put you there returns.")


# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================

def cell_1():

    global hasKey 
    # Introduce the scene to the player
    print("\nYou are in a small, dimly lit cell with an old wooden door. \nThe walls are made of cold stone, and the only source of light is a small window high up on the wall. \nThere is a small board held up by four tiny sticks and a pillow. \nYou think it is supposed to be a bed.")
    print() #empty line to separate text

    #Loop until player has key
    while hasKey == False:

    # Ask the player what they want to investigate
    # .lower() converts their answer to lowercase
     choice = input("What would you like to investigate?: ").lower().replace(" ", "")
     print() #empty line to separate text

    # Check whether the player chose the door
     if choice == "door":
        print("You approach the door. \nUppon close inspection, nothing seems amiss. \nYou can't see anything past the small grated hole in the door. It is too dark. \nAfter trying to open the door, you quickly realise it is locked. Why wouldn't it be?")
        print() #empty line to separate text

    # Check whether the player chose the window
     elif choice == "window":
        print("You approach the window. \nThe window is small and high up on the wall. \nThe sky is visible through the small opening, and it dark and devoid of any life. \nAfter trying to open the window, you stop and realise... you can't just push open iron bars.")
        print() #empty line to separate text

    # Check whether the player chose the bed
     elif choice == "bed":
        print("You approach the bed. \nThe bed is small and uncomfortable, with a lumpy pillow. \nYou notice that the bed is not bolted to the floor, and you think you might be able to move it. \nAfter little effort, you manage to move the bed and discover a small key hidden underneath it.")
    #Add key to inventory + end loop
        hasKey = True
        print() #empty line to separate text
        pouch.append("Iron Key")

    #If the player chooses none of the options    
     else:
        print("You decide not to investigate anything available in the cell. \nYou are left with the feeling that you are being watched.")
        print() #empty line to separate text


#============================================
# ESCAPE THE CASTLE - SCENE 2: THE HALLWAY  
#============================================

def hallway():
   
# Introduce the scene
 print("You unlock the door with the key and step into a pitch dark hallway. \nAfter letting your eyes adjust to the darkness for a few moments, you notice an old wooden cabinet.")
 print() #empty line to separate text
 pouch.remove("Iron Key")

 choice = input("Would you like to investigate the cabinet? yes/no ").lower().replace(" ", "")
 print() #empty line to separate text

 if choice == "yes" or choice == "y":
    print("You approach the cabinet. \nThe cabinet is old and dusty, with cobwebs covering the corners. \nYou open the cabinet and find a beautifully adorned dagger. \nYou take the dagger and add it to your pouch. \nYou decide to continue down the dark hallway, to the sound of your footsteps echoing.")
    print() #empty line to separate text

    pouch.append("Ritual Dagger")
    print(f"Your pouch now contains: {pouch}")
    print() #empty line to separate text

 elif choice == "no" or choice == "n":
    print("You decide not to investigate the cabinet. \nYou continue down the hallway, your footsteps echoing off the stone walls.")
    print() #empty line to separate text
    
#============================================
# ESCAPE THE CASTLE - SCENE 3: CORRIDOR ENCOUNTER
#============================================

# Define a function to describe an encounter
def encounter(random_creature):
    print("As you continue down the hallway...")
    print()#empty line to separate text
    
    # Randomly select a creature
    random_creature = random.choice(creatures)

# Different outcomes depending on the creature
    if random_creature == "Spiderling":
        print("You hear pattering, scurrying in your direction. \nYou have mere moments to react.")

    elif random_creature == "Scorned Spirit":
        print("A terrible wailing can be heard, louder by each passing second.")

    elif random_creature == "Cultist":
        print("From the darkness of the corridors you can faintly make out what seems to be a robed shape weilding adorned daggers.")

    print(f"A {random_creature} appears, ready to fight!")

# Pass the chosen creature into the encounter function
    encounter(random_creature)

#============================================
# ESCAPE THE CASTLE - SCENE 4: THE LIBRARY
#============================================

def library():
 
 global hasNote

#Introducing the scene
 print("After defeating the creature and continuing down the corridor, you find yourself in a library. \nThere are shelves stacked with books, stretching all the way from the floor to the ceiling. \nThe sheer size of this place is enough to leave you in awe.")
 print()
 print("It is still dark in here, save for scattered torches along the walls. \nUpon closer inspection, it becomes clear that this library hasn't seen any use in a very long time. \nThere is dust on the shelves and the books, as well as the tables and chairs. \nThere are cobwebs scattered in every empty nook and crany of this library.")

 #Loop until player has password
 while hasNote == False :

 #Investigation Choices
   choice  = input("What would you like to investigate?: ").lower().strip()
 #Password Investigation
   if choice in ("shelves", "the shelves", "shelf", "the shelf"):
    print("You walk past each and every shelf. Slowly. Looking for anything that may be out of place. \n... \n... \n... \nYou don't notice anything out of the ordinary... \nUntil you come to a sudden stop. \nThis shelf has no dust. The books aren't withering away. It's clean. \nAn uneasy feeling washes over you.")
    print()
    while True:
     shelf_choice = input("Do you wish to investigate this shelf?").lower().strip()

     if shelf_choice in ("yes", "y"):
       print("You decide to look through the shelf. \nAt first, no book seems to call your attention. \nAlbeit they seem significantly better preserved than its counterparts throughout the library, they all still seem ordinary. \nAll but one.\nOne of the books located on the shelf seems to be made of plastic. \nYou decide to pull it out, and upon closer inspection, it reveals to be a container rather than a book. \nYou open the container and inside find a piece of paper that reads: ")
       print()
       print("Hylenia")
       print()
       print("You put the piece of paper in your pouch, and decide to continue investigating the castle.")
       print() 
       #Add password to pouch
       pouch.append("Note - Hylenia")
       hasNote = True

     elif shelf_choice in ("no", "n"):
       print("You attempt to fight the urge to investigate this shelf, but ultimately, you cannot help but feel there is some importance to it")

     else:
       print("Please answer yes or no.")

 #Torch Investigation
   if choice in ("torches", "torch"):
    print("You decide to take a closer look at the torches in the library. \nIt wouldn't be a bad idea to take one of them with you as you explore. \nBut just as you're about to grab it, you take a second to think through it. \nCarrying a source of light with you will just alert others to your presence. \nMaybe it isn't such a good idea after all. \nYou decide to leave it alone.") 

#Table Investigation
   if choice in ("tables", "table", "chairs", "chair"):
    print("You approach one of the tables, but just like most things in this place, it contains nothing but dust. \nYou look closer, and see a tiny spider scurry through it. \nYou back away and continue your investigation.")
#Anything else
   else:
     print("I didn't quite understand what you wish to investigate. Please try again.")
