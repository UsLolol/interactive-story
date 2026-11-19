import os
import streamlit as st
import random
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
 
client = genai.Client(api_key=api_key) if api_key else None
 
MODEL_NAME = "gemini-3.5-flash-lite"
 
# ================================================================
# 1. PAGE SETUP — SAME APPROACH AS THE FINAL APP
# ================================================================
# page_icon uses the Unicode castle character, not an image file.
# Keep this before other Streamlit display calls.

st.set_page_config(page_title = "Escape the Castle", page_icon = "🏰", layout = "centered" )
st.title("🏰 Escape the Castle")

# ================================================================
# 2. GAME SETUP — INITIALISE VALUES ONCE
# ================================================================
# Session state remembers values when Streamlit reruns the script.

if "game_started" not in st.session_state:
    st.session_state.game_started = False

def start_game(name):
    st.session_state.game_started = True
    st.session_state.player_name = name
    st.session_state.health = 5
    st.session_state.max_health = 5
    st.session_state.pouch = []
    st.session_state.rooms = ["Cell", "Corridor", "Crypt", "Library", "Guard_Room", "Dungeon", "Castle_Gate"]
    st.session_state.room_number = 0
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False


def restart_game():
    st.session_state.clear()
    st.rerun()

def get_current_room():
    return st.session_state.rooms[st.session_state.room_number].lower()

def continue_game():
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False
    st.session_state.room_number += 1
    st.rerun()

def add_item(item):
    if item not in st.session_state.pouch:
        st.session_state.pouch.append(item)
 
def has_item(item):
    return item in st.session_state.pouch
 
def remove_item(item):
    if item in st.session_state.pouch:
        st.session_state.pouch.remove(item)

def take_damage(amount):
    st.session_state.health = st.session_state.health - amount
    if st.session_state.health < 0:
        st.session_state.health = 0

def heal_player(amount):
    old_health = st.session_state.health
    st.session_state.health = min(st.session_state.max_health, st.session_state.health + amount)
    return st.session_state.health - old_health

def generate_story(room, action, outcome, fallback_message):
    if client is None:
        return fallback_message

    pouch_text = ", ".join(st.session_state.pouch)

    prompt = f"""
You are the storyteller for a dark fantasy
adventure game called Escape the Castle.
 
Player: {st.session_state.player_name}
Room: {room}
Health: {st.session_state.health}/{st.session_state.max_health}
Inventory: {pouch_text}
 
Action:
{action}
 
Outcome:
{outcome}
 
Describe what happens in 30-50 words.
 
Use second person.
Use atmospheric dark fantasy language.
Do not change the outcome.
Do not change health or inventory.
Do not introduce new choices.
"""
    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
            generation_config={"thinking_level": "minimal"}
        )
        if interaction.output_text:
            return interaction.output_text
        return fallback_message
    except Exception as error:
        st.error(f"Gemini error: {error}")
        return fallback_message

def roll_dice():
    return random.randint(1,6)

def chance_encounter(room, action, success_number, success_outcome, success_fallback, failure_outcome, failure_fallback, damage, bonus_item=""):
    roll = roll_dice()
    bonus = 2 if bonus_item and has_item(bonus_item) else 0
    total = roll + bonus

    roll_message = (f"You rolled: {roll}")
    if bonus:
        roll_message += (f" + {bonus} equipment bonus!")
    roll_message += (f" = {total}.")

    if total >= success_number:
        story = generate_story(room, action, success_outcome, success_fallback)
        set_result("success", f"{roll_message} {story}")

    else:
        take_damage(damage)
        story = generate_story(room, action, failure_outcome, failure_fallback)
        set_result("damage", f"{roll_message} {story}", damage)


# ================================================================
# 3. REUSABLE DISPLAY FUNCTIONS — KEEP EVERY ROOM CONSISTENT
# ================================================================

#Showing the room
def show_room(title, description):
    st.header(title)
    st.write(description)

#Inventory Management
#Show player info
def show_player_info():
    st.subheader(f"👹 {st.session_state.player_name}")
    left, right = st.columns(2)
    with left:
        st.write(f"🩷 Health: {st.session_state.health} / {st.session_state.max_health}")
    with right: 
        st.write(f"🎒 Pouch: {', '.join(st.session_state.pouch)}")
    st.caption(
        f"Room {st.session_state.room_number + 1}"
        f" of {len(st.session_state.rooms)}"
    )
    st.divider()

def set_result(result_type, message, value = ""):
    st.session_state.result_type = result_type
    st.session_state.result_message = message
    st.session_state.result_value = value
    st.session_state.action_complete = True
    st.rerun()

def show_result():
    kind = st.session_state.result_type
    value = st.session_state.result_value
 
    if kind == "item":
        st.success(f"🎒 NEW ITEM: {value}")
    elif kind == "damage":
        st.error(f"💔 DAMAGE: You lose {value} health.")
    elif kind == "heal":
        st.success(f"💚 HEALED: You recover {value} health.")
    elif kind == "success":
        st.success("✅ Success!")
    else:
        st.info("The journey continues...")
 
    st.write(st.session_state.result_message)

#Continue button
def show_continue_button(text = "Continue"):
    if st.button(text):
        continue_game()

# ================================================================
# 4. START SCREEN — NAME INPUT FROM DAY 1
# ================================================================

if not st.session_state.game_started:
    st.write("You wake beneath an ancient castle. Your goal is to escape.")
    name = st.text_input("What is your name? ")

    if st.button("Enter the castle"):
        if name.strip():
            start_game(name)
            st.rerun()
        else:
            st.warning("Enter your name before starting your adventure ")
else:
    #Show the same player information in every room
    show_player_info()
    room = get_current_room()

    if st.session_state.health <= 0:
     show_room("💀 Game Over", "Your strength gives out. The castle has claimed another victim.")
     st.error("You did not escape the castle. Lol")
     if st.button("🔄 Try Again"):
        restart_game()
     st.stop()

    # ============================================================
    # ROOM 1 — CELL (MODEL SIMPLE CONTINUE NAVIGATION)
    # ============================================================
    if room == "cell":
        show_room("🔒 The Cell", " You wake on a cold stone floor. The iron door creaks open.")
        show_continue_button("🚪 Leave the cell")

    # ============================================================
    # ROOM 2 — CORRIDOR (MODEL RESULT -> CONTINUE)
    # ============================================================
    elif room == "corridor":
        show_room("🕯️ The Corridor", "A wooden cabinet stands beside the staircase.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🔎 Search the cabinet"):
                    outcome = "The player investigates the cabinet and finds a Rusty Dagger"
                    story = generate_story(
                        "The Corridor", "opens the cabinet", outcome, "You open the cabinet to find a rusty dagger within. You decide to take it with you."
                    )
                    add_item("Rusty Dagger")
                    set_result("item", story, "Rusty Dagger")
                    st.rerun()
                   
            with right:
                if st.button("Ignore cabinet"):
                    outcome = "The player leaves the cabinet alone and continues"
                    story = generate_story(
                        "The Corridor", "leaves the cabinet", outcome, "You decide to leave the cabinet alone and continue on your way."
                    )
                    set_result("story", story)
                    st.rerun()
        else:
            show_result()
            show_continue_button()

    # ============================================================
    # ROOM 3 — CRYPT
    # ============================================================
   
    #show_room("⚰️ The Crypt", "A metal object glints beside a stone coffin.")
    #Player should be given the choice to investigate the coffin or leave
    #If they do investigate they should obtain an Iron Key
    elif room == "crypt":
        show_room("⚰️ The Crypt", "A metal object glints beside a stone coffin.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🧩 Investigate the metal object"):
                    roll = roll_dice()
                    if roll >= 3:
                        add_item("Iron Key")
                        outcome = "The player investigates the metal object to find a key"
                        story = generate_story(
                        "The Crypt", "investigates the metal object", outcome, "You decide to investigate the glinting object and find an Iron Key. You decide to take it with you."
                        )
                        set_result("item", story , "Iron Key")
                    else:
                      take_damage(1)
                      set_result("damage", "You trip while attempting to grab the object and hurt yourself.", 1)
                      st.rerun()
            with right:
                if st.button("🚪 Ignore metal object"):
                    outcome = "The player decides to ignore the metal object and continues"
                    story = generate_story(
                        "The Crypt", "ignores the metal object", outcome, "You decide to leave the metal object alone and continue venturing further."
                    )
                    set_result("story", story)
                    st.rerun()
        else:
            show_result()
            show_continue_button()
 
    # ============================================================
    # ROOM 4 — LIBRARY
    # ============================================================
 
    #show_room("📚 The Forgotten Library", "A strange green light shines from an old book.")
    # Give the player the option to investigate or leave            
    elif room == "library":
        show_room("📚 The Forgotten Library", "A strange green light shines from an old book.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("📗 Look at the book closer..."):
                    roll = roll_dice()

                    if roll >= 5:
                      healed = heal_player(1)
                      outcome = "The player opens the book and is healed by its magic."
                      story = generate_story(
                        "The Library",
                        "opens the book",
                         outcome,
                         "As you open the mysterious book, your mind becomes flooded with ancient magic. This strange spell seems to have healed you."
                      )
                      set_result("heal", f"You rolled {roll}. {story}", healed)
                    else:
                        outcome = "The player opens the book, but nothing happens."
                        story = generate_story(
                            "The Library",
                            "opens book",
                            outcome,
                            "As you open the book, its light quickly dissipates before you can take a good look. Nothing happens."
                        )
                        set_result("story", f"You rolled {roll}. {story}")
            with right:
                if st.button("🚪 Leave the book alone."):
                    outcome = "The player leaves the book alone"
                    story = generate_story(
                        "The Library", "continues on their way", outcome, "You decide it is better to not mess with things you do not understand, and continue on your way."
                    )
                    set_result("story", story)
                    st.rerun()
        else:
            show_result()
            show_continue_button()

    # ============================================================
    # ROOM 5 — GUARD ROOM (CHOICES WITHOUT DICE YET)
    # ============================================================

    elif room == "guard_room":
        show_room("🗡️ The Guard Room", "A ghostly knight blocks the doorway.")
        if "Rusty Dagger" in st.session_state.pouch:
            st.info("You are carrying a Rusty Dagger.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("⚔️ Fight the knight"):
                    chance_encounter(
                        room="The Guard Room",
                        action="fights the ghostly knight",
                        success_number=4,
                        success_outcome="The player defeats the ghostly knight and can continue.",
                        success_fallback="You stand victorious over the knight's armour on the floor! A path forward presents itself.",
                        failure_outcome="The knight strikes the player, who loses 1 health and must try again.",
                        failure_fallback="The knight slashes your arm slightly. You lose 1 health point, but still have enough strength in you to try again.",
                        damage=1,
                        bonus_item="Rusty Dagger",
                    )
            with right:
                if st.button("🏃 Run past"):
                    outcome = "The player runs past the knight and can continue without injury"
                    story = generate_story(
                        "The Guard Room", "run past the knight", outcome, "You decide to run past the guard. You manage to sprint through without injury."
                    )
                    set_result("success", story)
                    st.rerun()
        else:
            show_result()
            if st.session_state.result_type == "damage":
                if st.button("Try fighting the knight again."):
                    st.session_state.action_complete = False
                    st.rerun()
            else:
               show_continue_button()

    # ============================================================
    # ROOM 6 — DUNGEON (INVENTORY PERSISTS ACROSS ROOMS)
    # ============================================================
    elif room == "dungeon":
        show_room("🦇 The Dungeon", "You enter a damp dungeon and see a bottle of red liquid.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            with left:
                if st.button("🍷 Take liquid"):
                    outcome = "The player takes the red liquid to find it is a healing potion"
                    story = generate_story(
                        "The Dungeon", "picks up the red liquid and finds it is a healing potion", outcome, "You take up the liquid to find it labeled as 'pick me up'."
                    )
                    add_item("Healing Potion")
                    set_result("item", story, "Healing Potion")
                    st.rerun()
            with right:
                if st.button("🤷 Ignore the liquid"):
                    outcome = "The player ignores the bottle and continues."
                    story = generate_story(
                        "The Dungeon", "ignores the bottle and continues", outcome, "You decide to leave the bottle alone and continue looking for a way out."
                    )
                    set_result("story", story)
                    st.rerun()
        else:
            show_result()
            show_continue_button()

#see a bottle of red liquid
#left - take it, find a healing potion
#right - leave it, leave the bottle behind
 
    # ============================================================
    # ROOM 7 — CASTLE GATE (BRANCH BASED ON INVENTORY)
    # ============================================================
    elif room == "castle_gate":
        show_room("⛩️ The Castle Gate", "You finally approach the castle gate, ready to escape.")
        if not st.session_state.action_complete:
            left, right = st.columns(2)
            if "Iron Key" in st.session_state.pouch:
                with left:
                    st.success("🗝️ You have the Iron Key.")
                    if st.button("🗝️ Unlock the castle gate"):
                        outcome = "The player unlocks the castle gate and escapes"
                        story = generate_story(
                            "Castle Gate", "unlocks the castle gate and escapes", outcome, "You unlock the castle gates with your iron key and alas, freedom!"
                        )
                        set_result("success", story)
                        st.rerun()
            else:
                with right:
                    st.warning("🔒 The gate is locked. You do not have the key.")
                    if st.button("🪜 Climb the wall"):
                            chance_encounter(
                               room="Castle Gate",
                               action="tries to climb the castle wall",
                               success_number=4,
                               success_outcome="The player climbs the wall and escapes.",
                               success_fallback="You make it over the wall. You are free!",
                               failure_outcome="The player falls while climbing and loses 1 health.",
                               failure_fallback="You slip and fall, losing 1 health.",
                               damage=1,
                            )

        else:
            show_result()

            if st.session_state.result_type == "damage":
                if st.session_state.health >=1:
                    if st.button("🪜 Try climbing again"):
                        st.session_state.action_complete = False
                        st.rerun()
            else:
              st.header("🏆 YOU ESCAPED THE CASTLE!")
              st.balloons()

        st.divider()
        if st.button("🔁 Play again"):
            restart_game()
#use the guard room as the template
#check to see if Iron Key held in inventory
#if key in inventory, show button to unlock the gate and escape
#if no key in inventiory show button to climb the wall and escape