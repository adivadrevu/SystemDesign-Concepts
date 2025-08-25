import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


app = FastAPI(title="Custom Article Cache Service")


cache: Dict[str, str] = {}

def fetch_article_from_server(url: str) -> str:
    print("Fetching article from server...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


class ArticleInput(BaseModel):
    url: str
    content: str

@app.get("/get/")
def get_article(url: str):
    print("Getting article...")
    if url not in cache:
        cache[url] = fetch_article_from_server(url)
    return {"url": url, "content": cache[url]}

@app.put("/put/")
def put_article(data: ArticleInput):
    print("Putting article in cache...")
    cache[data.url] = data.content
    return {"message": "Article cached successfully"}
