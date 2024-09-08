from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pytz
from Database_conn import COLLECTION_NAME, CONNECTION_STRING, DATABASE_NAME

# MongoDB connection
try:
    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to Cosmos MongoDB!")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")

# Helper Functions
def current_utc_time():
    india_timezone = pytz.timezone('Asia/Kolkata')
    dt = datetime.now(india_timezone)
    formatted_dt = dt.strftime('%d-%m-%Y %H-%M-%S')
    return formatted_dt

def Slug_Creation(st):
    return str('-'.join(st.split()))

def parse_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d-%m-%Y %H-%M-%S')

# Define your API routers
blog_create_router = APIRouter()
blog_detail_router = APIRouter()
slug_detail_router = APIRouter()

# Models
class Blogs(BaseModel):
    Title: str = Field(..., title="Blog Title", max_length=100)
    Description: str = Field(..., title="Blog Description", max_length=500)
    Image: Optional[str] = Field(None, title="Image URL")
    Author: str = Field(..., title="Author Name", max_length=100)
    Category: str = Field(..., title="Blog Category", max_length=50)
    Keyphrase: str = Field(..., title="Keyphrase", max_length=100)
    Metadescription: str = Field(..., title="Meta Description", max_length=160)
    MetaTitle: str = Field(..., title="Meta Title", max_length=60)
    DateTime: datetime = Field(default_factory=current_utc_time, title="Blog Creation Time")
    ScheduledTime: Optional[datetime] = Field(None, title="Scheduled Time")
    Keywords: str = Field(..., title="SEO Keywords", max_length=100)
    Slug: Optional[str] = Field(None, title="Slug", max_length=100)

class BlogSummary(BaseModel):
    Title: str
    thumbnail_image: Optional[str]
    DateTime: datetime
    Category: str
    Slug: str

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

# Create Blog API
@blog_create_router.post("/Create")
async def create_blog(blog: Blogs):
    try:
        if collection.find_one({"Title": blog.Title}):
            raise HTTPException(status_code=400, detail="Title already exists")
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

# List Blogs API
@blog_detail_router.get("/Getdetails", response_model=List[BlogSummary])
def list_blogs():
    try:
        blogs_cursor = collection.find({}, {"_id": 0, "Title": 1, "Image": 1, "DateTime": 1, "Slug": 1, "Category": 1})
        blogs_list = list(blogs_cursor)

        if not blogs_list:
            raise HTTPException(status_code=404, detail="No blogs found")

        return [
            BlogSummary(
                Title=blog["Title"],
                thumbnail_image=blog.get("Image"),
                DateTime=parse_datetime(blog["DateTime"]),
                Category=blog["Category"],
                Slug=blog["Slug"]
            ) for blog in blogs_list
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving blogs: {e}")

# Get Blog Details by Slug API
@slug_detail_router.get("/{slug}", response_model=BlogDetails)
def get_blog_details(slug: str):
    blog = collection.find_one({"Slug": slug})

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    try:
        return BlogDetails(
            Title=blog["Title"],
            Description=blog["Description"],
            Image=blog.get("Image"),
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

# Main FastAPI app
app = FastAPI()

# Include Routers
app.include_router(blog_create_router, prefix="/blog")
app.include_router(blog_detail_router, prefix="/blogs")
app.include_router(slug_detail_router, prefix="/blog")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app , port=8000)
