from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class UserCaptions(Base):
    __tablename__ = 'user_captions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    captions = Column(JSONB, nullable=False)
    processed_captions = Column(JSONB, nullable=False)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
