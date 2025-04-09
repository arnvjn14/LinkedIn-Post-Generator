import streamlit as st
from data_adder import save_entries_to_database
from database.models import SessionLocal, UserCaptions
from preprocess import process_posts
from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def main():
    name = st.text_input("Enter your name:", placeholder="Type your full name here")
    dob=st.date_input("Enter your Date of Birth:")


    if name:
        st.subheader(f"Hello, {name}!")

    
    if "entries" not in st.session_state:
        st.session_state.entries = []

    with st.form("input_form"):
        text = st.text_area("Enter your text:", placeholder="Type your text here")
        engagement = st.number_input("Enter engagement (numeric):", min_value=0, step=1)
        add_button = st.form_submit_button("Add Entry")

        if add_button:
            if text:
                st.session_state.entries.append({"text": text, "engagement": engagement})
                st.success("Entry added successfully!")
            else:
                st.error("Please enter some text before adding.")

    # Display all entries
    if st.session_state.entries:
        st.subheader("All Entries:")
        for idx, entry in enumerate(st.session_state.entries, start=1):
            st.write(f"**Entry {idx}:**")
            st.write(f"- **Text:** {entry['text']}")
            st.write(f"- **Engagement:** {entry['engagement']}")

    if st.button("Save Entries to JSON"):

        save_entries_to_database(name,dob)
        st.session_state.entries = []
        process_posts(name,dob)
        st.rerun()




        # save_entries_to_json()
        # st.session_state.entries = []  # Clear session state after saving
        # st.experimental_rerun()  # Refresh the app

    # Reset option
    if st.button("Reset All Entries"):
        st.session_state.entries = []
        st.experimental_rerun()
        st.success("All entries have been cleared!")

    
    st.subheader("LinkedIn Post Generator:")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts(name,dob)
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)



    # Generate Button
    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag,name,dob)
        st.write(post)   

if __name__ == "__main__":
    main()





