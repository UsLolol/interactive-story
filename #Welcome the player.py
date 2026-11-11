#Welcome the player
print("=== ESCAPE THE CASTLE ===")
print("Welcome, adventurer!")
#Get player name, age and character class
playerName = input("Please state your name")
playerAge = int(input("Please state your age"))
playerClass = input("What is your preferred class?")
 
#Set starting values
health = 100
gold = 20
hasKey = False
 
#Display the character profile
print("\n=== YOUR CHARACTER PROFILE ===")
print(f"Name: {playerName}")
print(f"Age: {playerAge}")
print(f"Class: {playerClass}")
print(f"Health: {health}")
print(f"Gold: {gold}")
print(f"Has Escape Key: {hasKey}")

#Begin the story
print(f"You, {playerName}, wake up in a damp and dark cell.")
print("The air is thick with the smell of mold and decay.")
print("You can hear the distant sound of dripping water echoing through the stone corridors.")
print("You have no memory of how you got here, but you know you must escape before whoever has put you there returns.")


# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================

# Introduce the scene to the player
print("\nYou are in a small, dimly lit cell with an old wooden door. \nThe walls are made of cold stone, and the only source of light is a small window high up on the wall. \nThere is a small board held up by four tiny sticks and a pillow. \nYou think it is supposed to be a bed.")

# Ask the player what they want to investigate
# .lower() converts their answer to lowercase
choice = input("What would you like to investigate?").lower().replace(" ", "")

# Check whether the player chose the door
if choice == "door":
    print("You approach the door. \nUppon close inspection, nothing seems amiss. \nYou can't see anything past the small grated hole in the door. It is too dark. \nAfter trying to open the door, you quickly realise it is locked. Why wouldn't it be?")

# Check whether the player chose the window
elif choice == "window":
    print("You approach the window. \nThe window is small and high up on the wall. \nThe sky is visible through the small opening, and it dark and devoid of any life. \nAfter trying to open the window, you stop and realise... you can't just push open iron bars.")

# Check whether the player chose the bed
elif choice == "bed":
    print("You approach the bed. \nThe bed is small and uncomfortable, with a lumpy pillow. \nYou notice that the bed is not bolted to the floor, and you think you might be able to move it. \nAfter little effort, you manage to move the bed and discover a small key hidden underneath it.")

else:
    print("You decide not to investigate anything in the cell. \nYou are left with the feeling that you are being watched.")