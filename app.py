import streamlit as st
#!!!!!!!!  python -m streamlit run app.py

# STEP 1 — Initialise game values once per browser session.
# Streamlit reruns the script when the player interacts with a widget.
# These values need to survive those reruns.
if "playerName" not in st.session_state:
    st.session_state.playerName = ""

if "health" not in st.session_state:
    st.session_state.health = 100

if "pouch" not in st.session_state:
    st.session_state.pouch = []

if "scene" not in st.session_state:
    st.session_state.scene = "Start"

if "result" not in st.session_state:
    st.session_state.result = ""

# STEP 2 — Show the game's title and the information the player carries.

st.title("Escape The Castle")

if st.session_state.playerName:
    st.write(f"Player: {st.session_state.playerName}")
    st.write(f"Health: {st.session_state.health}")
    st.write(f"Pouch: {st.session_state.pouch}")

# STEP 3 — Start screen: use a text input and button.
# The name is saved to session state so it is available in later scenes.

if st.session_state.scene == "Start":
    st.subheader("Create Your Character")
    st.session_state.playerName = st.text_input("What is your name?")
    if st.button("Start Adventure"):
        st.session_state.scene = "Cell"
        st.rerun()

# STEP 4 — Cell scene: convert the terminal choices into buttons.
# Store the result so it stays visible after other interactions.

elif st.session_state.scene == "Cell":
    st.subheader("The Cell")
    st.write("You wake up in a dark castle cell.")
    st.write("You can see a door, a window, and an old bed.")

    if st.button("Investigate the door"):
        st.session_state.result = "The door is locked, you need a key."

    if st.button("Invesigate the window"):
        st.session_state.result = "The window is too small to fit through."

    if st.button("Investigate the bed"):
        if "Iron Key" not in st.session_state.pouch:
            st.session_state.pouch.append("Iron Key")
            st.session_state.result = "You have found an Iron Key!"
        else:
            st.session_state.result = "There is nothing else under the bed."

    if st.session_state.result:
        st.info(st.session_state.result)

# STEP 5 — Unlock progress using a condition based on inventory.
    if "Iron Key" in st.session_state.pouch:
        if st.button("Unlock the door and continue"):
            st.session_state.scene = "Corridor"
            st.session_state.result = ""
            st.rerun()

# STEP 6 — Corridor scene: use the SAME inventory as in the Cell.

# Initialise the corridor scene - the player needs to notice a cabinet
elif st.session_state.scene == "Corridor":
    st.subheader("You enter the corridor")
    st.write("You notice an old cabinet")

    # Give the player options to "Open the cabinet" or "Leave the cabinet"
    # If the player opens the cabinet, they should find a rusty dagger
    if st.button("Open the cabinet"):
        if "Rusty Dagger" not in st.session_state.pouch:
            st.session_state.pouch.append("Rusty Dagger")
            st.session_state.result = "You open the cabinet, and inside find a rusty dagger!"
        else:
            st.session_state.result = "The cabinet is empty."

    if st.button("Leave the cabinet"):
        st.session_state.result = "You leave the cabinet alone"

    if st.session_state.result:
        st.info(st.session_state.result)

        # Allow the player to continue with or without the dagger
        if st.button("Continue"):
            st.session_state.scene = "Continue"
            st.session_state.result = ""
            st.rerun()