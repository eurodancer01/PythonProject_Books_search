from fastapi import FastAPI, HTTPException,Query,Request
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import httpx
from typing import List
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

with open("templates/homepage.html", "r") as html_file:
    homepage_html_content = html_file.read()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return homepage_html_content


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):

    url = f"https://books-api7.p.rapidapi.com/books/{book_id}"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/find_book_by_author/")
async def find_book_by_author(lname: str, fname: str):
    url = "https://books-api7.p.rapidapi.com/books/find/author"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"lname": lname, "fname": fname}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()


@app.get("/find_books_by_genres/")
async def find_books_by_genres(genres: List[str] = Query(["fantasy", "fiction", "Classics"])):
    url = "https://books-api7.p.rapidapi.com/books/find/genres"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"genres[]": genres}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@app.get("/find_books_by_rating/")
async def find_books_by_rating(lte: str, gte: str, p: str):
    url = "https://books-api7.p.rapidapi.com/books/find/rating"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",  # Ensure to replace YOUR_API_KEY with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"lte": lte, "gte": gte, "p": p}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()

@app.get("/find_book_by_title/")
async def find_book_by_title(title: str):
    url = "https://books-api7.p.rapidapi.com/books/find/title"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"title": title}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
