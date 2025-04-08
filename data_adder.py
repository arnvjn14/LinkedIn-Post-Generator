import os
import streamlit as st
from database.models import SessionLocal, UserCaptions
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def save_entries_to_database(name,dob):
    # st.success("Captions submitted successfully!")
    if name and dob:
        session: Session=SessionLocal()
        try:
            user = session.query(UserCaptions).filter_by(name=name, dob=dob).first()
            if user:
                print(user.captions)
                print(st.session_state.entries)
                combined_array = user.captions + st.session_state.entries
                user.captions=combined_array
                st.success("Captions submitted successfully!")
            else:
                user = UserCaptions(
                    name=name,
                    dob=dob,
                    captions=st.session_state.entries,
                    processed_captions=[]  
                )
                session.add(user)
                session.commit()
                st.success("Captions submitted successfully!")
        except SQLAlchemyError as e:
            session.rollback()
            st.error(f"An error occurred: {str(e)}")
        finally:
            session.close()
    else:
        st.error("Please fill in all fields.")






        
        