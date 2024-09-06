from fastapi import FastAPI,HTTPException,APIRouter
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from Database_conn import COLLECTION_NAME,CONNECTION_STRING,DATABASE_NAME
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pytz


# 1)Create Blog (POST):
# Title, Description, Image, Author, 
# Category, DateTime, Shceduled Time(optional), 
# Keyphrase, Metadescription, MetaTitle, Keywords(tags).

# Replace with your actual connection string and database/collection details
# Connect to Cosmos DB using MongoDB API

try:
    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to Cosmos MongoDB!")  
except ConnectionFailure as e:
    print(f"Connection failed: {e}")


app = FastAPI()

def current_utc_time():
    india_timezone = pytz.timezone('Asia/Kolkata')
    dt = datetime.now(india_timezone)
    formatted_dt = dt.strftime('%d-%m-%Y   %H-%M-%S')
    return formatted_dt

def Slug_Creation(st):
    return str('-'.join(st.split()))

class Blogs(BaseModel):
    Title: str = Field(..., title="Blog Title", max_length=100)
    Description: str = Field(..., title="Blog Description", max_length=500)
    Image: Optional[str] = Field(None, title="Image URL")
    Author: str = Field(..., title="Author Name", max_length=100)
    Category: str = Field(..., title="Blog Category", max_length=50)
    Keyphrase: str = Field(..., title="Keyphrase",max_length= 100)
    Metadescription: str = Field(..., title="Meta Description", max_length=160)
    MetaTitle: str = Field(..., title="Meta Title", max_length=60)
    DateTime: datetime = Field(default_factory = current_utc_time, title="Blog Creation Time")
    ScheduledTime: Optional[datetime] = Field(None, title="Scheduled Time")
    Keywords: str = Field(..., title="SEO Keywords", max_length=100)
    Slug : Optional[str] = Field(None,title = 'Shown the blogs', max_length=100)

@app.post("/create a blog")
async def create_blog(blog: Blogs):
    try:
        # Convert Pydantic model to dict

        if collection.find_one({"Title": blog.Title}):
            raise HTTPException(status_code=400, detail="Title is already exists")
        else:
             
             blog.Slug = Slug_Creation(blog.Title)
             blog_data = blog.model_dump()
             result = collection.insert_one(blog_data)
        
        return {
            "message": "Blog created successfully",
            "blog_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create blog: {e}")
    

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)