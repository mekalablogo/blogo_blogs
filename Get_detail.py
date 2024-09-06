from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
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

# Blog summary model for listing blogs
class BlogSummary(BaseModel):
    Title: str
    thumbnail_image: Optional[str]  # Ensure consistency with MongoDB field names
    DateTime: datetime
    Category: str
    Slug: str

app = FastAPI()


def parse_datetime(date_str: str) -> datetime:
    # Adjust this format according to your MongoDB date format
    return datetime.strptime(date_str, '%d-%m-%Y   %H-%M-%S')


# 1. List of Blogs (Title, thumbnail image, datetime, slug, category)
@app.get("/blogs/", response_model=List[BlogSummary])
def list_blogs():
    try:
        blogs_cursor = collection.find({}, {"_id": 0, "Title": 1, "Image": 1, "DateTime": 1, "Slug": 1, "Category": 1})
        blogs_list = list(blogs_cursor)  # Convert cursor to a list

        # If no blogs found
        if not blogs_list:
            raise HTTPException(status_code=404, detail="No blogs found")

        # Map the result to the BlogSummary model
        blog_list = [
            BlogSummary(
                Title=blog["Title"],
                thumbnail_image=blog.get("Image"),  # Optional image URL
                DateTime = parse_datetime(blog["DateTime"]),
                Category=blog["Category"],
                Slug=blog["Slug"]
            ) for blog in blogs_list
        ]

        return blog_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving blogs: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
