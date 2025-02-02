import streamlit as st



def main():
    name = st.text_input("Enter your name:", placeholder="Type your name here")

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

    # Reset option
    if st.button("Reset All Entries"):
        st.session_state.entries = []
        st.experimental_rerun()
        st.success("All entries have been cleared!")

if __name__ == "__main__":
    main()





