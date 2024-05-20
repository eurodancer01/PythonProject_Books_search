from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI()


@app.get("/books/random")
async def get_random_book():
    url = "https://books-api7.p.rapidapi.com/books/get/random/"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",  # Replace with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # This will raise an exception for HTTP error responses
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=response.status_code, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
