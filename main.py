from fastapi import FastAPI
from Blogo_Post import Blog_create
from Get_detail import Blog_detail
from Slug_based import Slug_detail

app = FastAPI()

# Mount the individual applications with prefixes
app.mount("/blog/create", Blog_create)
app.mount("/blog/details", Blog_detail)
app.mount("/blog", Slug_detail)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
