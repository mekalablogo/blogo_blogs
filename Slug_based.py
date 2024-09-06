from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from Database_conn import COLLECTION_NAME, CONNECTION_STRING, DATABASE_NAME

# MongoDB connection
try:
    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to Cosmos MongoDB!")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")

# Blog details model
class BlogDetails(BaseModel):
    Title: str
    Description: str
    Image: Optional[str]
    Author: str
    Category: str
    DateTime: datetime
    ScheduledTime: Optional[datetime]
    Keyphrase: str
    Metadescription: str
    MetaTitle: str
    Slug: str

Slug_detail = FastAPI()

def parse_datetime(date_str: str) -> datetime:
    # Adjust this format according to your MongoDB date format
    return datetime.strptime(date_str, '%d-%m-%Y %H-%M-%S')

# Get blog details by slug
@app.get("/Blogs/{slug}", response_model=BlogDetails)
def get_blog_details(slug: str):
    blog = collection.find_one({"Slug": slug})

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Ensure all fields exist and have correct types
    try:
        return BlogDetails(
            Title=blog["Title"],
            Description=blog["Description"],
            Image=blog.get("Image"),  # Optional image URL
            Author=blog["Author"],
            Category=blog["Category"],
            DateTime=parse_datetime(blog["DateTime"]),
            ScheduledTime=blog.get("ScheduledTime"),
            Keyphrase=blog["Keyphrase"],
            Metadescription=blog["Metadescription"],
            MetaTitle=blog["MetaTitle"],
            Slug=blog["Slug"]
        )
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing field in blog document: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing date: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
