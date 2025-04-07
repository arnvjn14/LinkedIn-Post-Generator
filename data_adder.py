import os
import json
import streamlit as st

FILE_PATH = "./data/raw_posts.json"

# def load_existing_entries():
#     """Loads existing entries from the JSON file if it exists."""
#     if os.path.exists(SAVE_PATH):
#         with open(SAVE_PATH, "r", encoding="utf-8") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return []  # Return empty list if JSON is corrupted
#     return []

# def save_entries_to_json():
#     """Appends new session state entries to the existing JSON file."""
#     if not st.session_state.entries:
#         st.error("No new entries to save!")
#         return

#     # Load existing data
#     existing_data = load_existing_entries()

#     # Append new entries
#     existing_data.extend(st.session_state.entries)

#     # Ensure the directory exists
#     os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

#     # Save the updated list to JSON
#     with open(SAVE_PATH, "w", encoding="utf-8") as f:
#         json.dump(existing_data, f, indent=4, ensure_ascii=False)

#     st.success(f"Entries successfully saved to {SAVE_PATH}!")






# import streamlit as st
# import json
# import os

# # Define the file path for saving JSON data
# SAVE_PATH = "data/raw_posts.json"


def load_existing_entries():
    """Loads existing entries from the JSON file if it exists."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # Load existing data
            except json.JSONDecodeError:
                return []  # Return empty list if JSON is corrupted
    return []

def save_entries_to_json():
    """Appends new session state entries to the existing JSON file while handling Unicode characters properly."""
    if not st.session_state.entries:
        st.error("No new entries to save!")
        return

    # Load existing data
    existing_data = load_existing_entries()

    # Append new entries
    existing_data.extend(st.session_state.entries)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # Save the updated list to JSON with proper UTF-8 encoding
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    st.success(f"Entries successfully saved to {FILE_PATH}!")