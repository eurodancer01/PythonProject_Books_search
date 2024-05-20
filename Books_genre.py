from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import json


app = FastAPI()

API_KEY = "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53"
API_HOST = "books-api7.p.rapidapi.com"
URL = f"https://{API_HOST}/books/find/genres"


@app.get("/books/find/genres")
async def find_books_by_genres():
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    querystring = {"genres[]": ["fantasy", "fiction", "Classics"]}

    response = requests.get(URL, headers=headers, params=querystring)

    json_response = response.json()
    indented_json_response = json.dumps(json_response, indent=5)
    html_content = json_to_html(indented_json_response)

    return html_content




def json_to_html(json_data):
    html_content = "<ul>"
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            html_content += f"<li><strong>{key}:</strong> {json_to_html(value)}</li>"
    elif isinstance(json_data, list):
        for item in json_data:
            html_content += f"<li>{json_to_html(item)}</li>"
    else:
        html_content += str(json_data)
    html_content += "</ul>"
    return HTMLResponse(content=html_content)


if __name__=="__main__":
    uvicorn.run(app)