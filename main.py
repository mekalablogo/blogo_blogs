from fastapi import FastAPI
from Blog_Post import Blog_create
from Get_detail import Blog_detail
from Slug_based import Slug_detail

app = FastAPI()

# Include the other applications
app.mount("/Create a blog", Blog_create)
app.mount("/GetDetail", Blog_detail)
app.mount("/Blogs/{slug}", Slug_detail)
