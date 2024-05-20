from fastapi import FastAPI, HTTPException
from typing import Optional
import requests,uvicorn

app = FastAPI()


@app.get("/books/find/title")
async def find_book_by_title(title: Optional[str] = None):
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    url = "https://books-api7.p.rapidapi.com/books/find/title"
    querystring = {"title": title}
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching book data")

    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
