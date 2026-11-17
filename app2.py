import streamlit as st
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
    return st.session_state.rooms[st.session_state.room_number]

def continue_game():
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False
    st.session_state.room_number += 1
    st.rerun()

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
    message = st.session_state.result_message
    if kind == "item":
        st.success(f"🎒 NEW ITEM: {st.session_state.result_value}")
        st.write(message)
    elif kind == "success":
        st.success(message)
    else:
        st.info(message)

def add_item(item):
    if item not in st.session_state.pouch:
        st.session_state.pouch.append(item)

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
                    add_item("Rusty Dagger")
                    set_result("item", "You find a Rusty Dagger inside the cabinet.", "Rusty Dagger")
            with right:
                if st.button("Ignore cabinet"):
                    set_result("story", "You leave the cabinet alone and walk onwards.")
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
                    add_item("Iron Key")
                    set_result("item", "You find an Iron Key beside the coffin.", "Iron Key")
            with right:
                if st.button("🚪 Ignore metal object"):
                    set_result("story", "You ignore the glistening object and continue through the crypt.")
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
                    set_result("story", "You open the book to find your mind flooded with ancient spells.")
            with right:
                if st.button("🚪 Leave the book alone."):
                    set_result("story", "You decide to not mess with things you do not understand.")
        else:
            show_result()
            show_continue_button()