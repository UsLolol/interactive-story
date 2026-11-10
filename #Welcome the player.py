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
print(f"\n You, {playerName}, wake up in a damp and dark cell.")
print("The air is thick with the smell of mold and decay.")
print("You can hear the distant sound of dripping water echoing through the stone corridors.")
print("You have no memory of how you got here, but you know you must escape before whoever has put you there returns.")
