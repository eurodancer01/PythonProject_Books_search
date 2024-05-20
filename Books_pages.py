from fastapi import FastAPI, HTTPException
import requests,uvicorn

app = FastAPI()

@app.get("/books/by-page")
async def get_books_by_page(page: int):
    url = "https://books-api7.p.rapidapi.com/books"
    querystring = {"p": str(page)}
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raises an exception for HTTP errors
        print(response.json())
        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

