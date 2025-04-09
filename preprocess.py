import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from database.models import UserCaptions, SessionLocal
from sqlalchemy.orm import Session


# def process_posts(raw_file_path, processed_file_path=None):
#     with open(raw_file_path, encoding='utf-8') as file:
#         posts = json.load(file)
#         enriched_posts = []
#         for post in posts:
#             metadata = extract_metadata(post['text'])
#             post_with_metadata = post | metadata
#             enriched_posts.append(post_with_metadata)

#     unified_tags = get_unified_tags(enriched_posts)
#     for post in enriched_posts:
#         current_tags = post['tags']
#         new_tags = {unified_tags[tag] for tag in current_tags}
#         post['tags'] = list(new_tags)

#     with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
#         json.dump(enriched_posts, outfile, indent=4)

def process_posts(name,dob):
    session=SessionLocal()
    try:
        user = session.query(UserCaptions).filter(
             UserCaptions.name == name,
             UserCaptions.dob == dob
         ).first()
        
        if not user:
            raise ValueError(f"User not found with name: {name} and DOB: {dob}")
        
        posts = user.captions

        enriched_posts = []

        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

        unified_tags = get_unified_tags(enriched_posts)
        for post in enriched_posts:
            current_tags = post['tags']
            new_tags = {unified_tags[tag] for tag in current_tags}
            post['tags'] = list(new_tags)

        if user.processed_captions:
            
            user.processed_captions = user.processed_captions + enriched_posts
        else:
            
            user.processed_captions = enriched_posts
        
        # Commit changes to the database
        session.commit()
        
        return enriched_posts
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  # Add the tags to the set

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


if __name__ == "__main__":
    
    name = "John Doe"
    dob = "1990-01-01"  
    
    try:
        processed_posts = process_posts(name, dob)
        print(f"Successfully processed {len(processed_posts)} posts for {name}")
    except Exception as e:
        print(f"Error processing posts: {str(e)}")




# import json
# import os
# from sqlalchemy import create_engine, Column, Integer, String, Date, JSONB
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from llm_helper import llm
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException

# # Database model setup
# Base = declarative_base()

# class UserCaptions(Base):
#     __tablename__ = 'user_captions'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     dob = Column(Date, nullable=False)
#     captions = Column(JSONB, nullable=False)
#     processed_captions = Column(JSONB, nullable=False)


# def process_posts_from_db(user_name, user_dob):
#     # Setup database connection
#     DATABASE_URL = os.getenv("DATABASE_URL")
#     engine = create_engine(DATABASE_URL)
#     SessionLocal = sessionmaker(bind=engine)
#     session = SessionLocal()
    
#     try:
#         # Find user by name and dob
#         user = session.query(UserCaptions).filter(
#             UserCaptions.name == user_name,
#             UserCaptions.dob == user_dob
#         ).first()
        
#         if not user:
#             raise ValueError(f"User not found with name: {user_name} and DOB: {user_dob}")
        
#         # Extract raw captions
#         posts = user.captions
        
#         # Process the posts
#         enriched_posts = []
#         for post in posts:
#             metadata = extract_metadata(post['text'])
#             post_with_metadata = post | metadata
#             enriched_posts.append(post_with_metadata)

#         # Unify tags
#         unified_tags = get_unified_tags(enriched_posts)
#         for post in enriched_posts:
#             current_tags = post['tags']
#             new_tags = {unified_tags[tag] for tag in current_tags}
#             post['tags'] = list(new_tags)
        
#         # Update the user's processed_captions in the database
#         if user.processed_captions:
#             # Append new processed captions to existing ones
#             user.processed_captions = user.processed_captions + enriched_posts
#         else:
#             # Initialize processed_captions if it's empty
#             user.processed_captions = enriched_posts
        
#         # Commit changes to the database
#         session.commit()
        
#         return enriched_posts
        
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()


# def extract_metadata(post):
#     template = '''
#     You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
#     1. Return a valid JSON. No preamble. 
#     2. JSON object should have exactly three keys: line_count, language and tags. 
#     3. tags is an array of text tags. Extract maximum two tags.
#     4. Language should be English or Hinglish (Hinglish means hindi + english)
    
#     Here is the actual post on which you need to perform this task:  
#     {post}
#     '''

#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={"post": post})

#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#     return res


# def get_unified_tags(posts_with_metadata):
#     unique_tags = set()
#     # Loop through each post and extract the tags
#     for post in posts_with_metadata:
#         unique_tags.update(post['tags'])  # Add the tags to the set

#     unique_tags_list = ','.join(unique_tags)

#     template = '''I will give you a list of tags. You need to unify tags with the following requirements,
#     1. Tags are unified and merged to create a shorter list. 
#        Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
#        Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
#        Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
#        Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
#     2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
#     3. Output should be a JSON object, No preamble
#     3. Output should have mapping of original tag and the unified tag. 
#        For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
#     Here is the list of tags: 
#     {tags}
#     '''
#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={"tags": str(unique_tags_list)})
#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#     return res


# if __name__ == "__main__":
#     # Example usage: process posts for a specific user
#     user_name = "John Doe"
#     user_dob = "1990-01-01"  # Format: YYYY-MM-DD
    
#     try:
#         processed_posts = process_posts_from_db(user_name, user_dob)
#         print(f"Successfully processed {len(processed_posts)} posts for {user_name}")
#     except Exception as e:
#         print(f"Error processing posts: {str(e)}")