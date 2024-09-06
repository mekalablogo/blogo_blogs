from fastapi import FastAPI
from Blog_Post import Blog_create
from Get_detail import Blog_detail
from Slug_based import Slug_detail

app = FastAPI()

app.include_router(Blog_create, prefix="/blog/create")
app.include_router(Blog_detail, prefix="/blog/details")
app.include_router(Slug_detail, prefix="/blog")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}
