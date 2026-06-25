from fastapi import FastAPI
from routers import download, general, upload

app = FastAPI(title="title", description="description", version="0.1.0")
app.include_router(upload.router)
app.include_router(download.router)
app.include_router(general.router)


@app.get("/")
def root():
    return {"message": "Hello world"}
