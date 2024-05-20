from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.get("/movies/{title}")
async def get_movies_by_title(title: str):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"title": title}
    headers = {
        "Type": "get-movies-by-title",
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return JSONResponse(content=response.json())
