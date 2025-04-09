import pandas as pd
import json
from database.models import SessionLocal, UserCaptions


class FewShotPosts:
    def __init__(self, name=None, dob=None):
        self.df = None
        self.unique_tags = None
        self.load_posts_from_db(name, dob)
    
    def load_posts_from_db(self, name, dob):
        session = SessionLocal()
        try:
            # Find the user by name and dob
            query = session.query(UserCaptions)
            if name:
                query = query.filter(UserCaptions.name == name)
            if dob:
                query = query.filter(UserCaptions.dob == dob)
            
            user = query.first()
            
            if not user or not user.processed_captions:
                raise ValueError("User not found or processed_captions is empty")
            
            # Convert the JSONB processed_captions to pandas DataFrame
            posts = user.processed_captions
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            
            # Collect unique tags
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))
            
        finally:
            session.close()

    def get_filtered_posts(self, length, language, tag):
        if self.df is None:
            return []
            
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &  # Tags contain specified tag
            (self.df['language'] == language) &  # Language matches specified language
            (self.df['length'] == length)  # Length category matches specified length
        ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags
    
if __name__ == "__main__":
    
    name = "John Doe"
    dob = "1990-01-01" 
    
    fs = FewShotPosts(name, dob)
    
    # Print available tags
    print("Available tags:", fs.get_tags())
    
    # Get medium length Hinglish posts related to Job Search
    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(f"Found {len(posts)} 'Job Search' posts in Hinglish of medium length")
    print(posts)


# import pandas as pd
# import json
# from sqlalchemy import create_engine, Column, Integer, String, Date, JSONB
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# Base = declarative_base()

# class UserCaptions(Base):
#     __tablename__ = 'user_captions'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     dob = Column(Date, nullable=False)
#     captions = Column(JSONB, nullable=False)
#     processed_captions = Column(JSONB, nullable=False)


# class FewShotPosts:
#     def __init__(self, database_url=None, user_name=None, user_dob=None):
#         self.df = None
#         self.unique_tags = None
#         self.database_url = database_url or os.getenv("DATABASE_URL")
#         self.engine = create_engine(self.database_url)
#         self.SessionLocal = sessionmaker(bind=self.engine)
#         self.load_posts_from_db(user_name, user_dob)

#     def load_posts_from_db(self, user_name, user_dob):
#         session = self.SessionLocal()
#         try:
#             # Find the user by name and dob
#             query = session.query(UserCaptions)
#             if user_name:
#                 query = query.filter(UserCaptions.name == user_name)
#             if user_dob:
#                 query = query.filter(UserCaptions.dob == user_dob)
            
#             user = query.first()
            
#             if not user or not user.processed_captions:
#                 raise ValueError("User not found or processed_captions is empty")
            
#             # Convert the JSONB processed_captions to pandas DataFrame
#             posts = user.processed_captions
#             self.df = pd.json_normalize(posts)
#             self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            
#             # Collect unique tags
#             all_tags = self.df['tags'].apply(lambda x: x).sum()
#             self.unique_tags = list(set(all_tags))
            
#         finally:
#             session.close()

#     def get_filtered_posts(self, length, language, tag):
#         if self.df is None:
#             return []
            
#         df_filtered = self.df[
#             (self.df['tags'].apply(lambda tags: tag in tags)) &  # Tags contain specified tag
#             (self.df['language'] == language) &  # Language matches specified language
#             (self.df['length'] == length)  # Length category matches specified length
#         ]
#         return df_filtered.to_dict(orient='records')

#     def categorize_length(self, line_count):
#         if line_count < 5:
#             return "Short"
#         elif 5 <= line_count <= 10:
#             return "Medium"
#         else:
#             return "Long"

#     def get_tags(self):
#         return self.unique_tags


# if __name__ == "__main__":
#     # Example usage
#     database_url = os.getenv("DATABASE_URL")
    
#     # Find posts for a specific user by name and date of birth
#     user_name = "John Doe"
#     user_dob = "1990-01-01"  # Format: YYYY-MM-DD
    
#     fs = FewShotPosts(database_url, user_name, user_dob)
    
#     # Print available tags
#     print("Available tags:", fs.get_tags())
    
#     # Get medium length Hinglish posts related to Job Search
#     posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
#     print(f"Found {len(posts)} 'Job Search' posts in Hinglish of medium length")
#     print(posts)