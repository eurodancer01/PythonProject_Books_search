from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from collections import Counter
import json
import http.client
import base64
from io import BytesIO
from food import get_recipe, extract_categories, extract_nutritional_info  # Import relevant functions from food.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import httpx
import subprocess
from typing import List

app = FastAPI()


# Mount the directory containing static files (e.g., JavaScript files) to a specific path
app.mount("/static", StaticFiles(directory="."), name="static")

# Define HTML content for each endpoint
endpoints_content = {
    "hearthstone": "<h1>Hearthstone</h1><p>This is the Hearthstone endpoint.</p>",
    "food": "<h1>Food</h1><p>This is the Food endpoint.</p>",
    "movies": "<h1>Movies</h1><p>This is the Movies endpoint.</p>",
    "books": "<h1>Books</h1><p>This is the Books endpoint.</p>",
    "shows": "<h1>Shows</h1><p>This is the Shows endpoint.</p>"
}

# Define routes for each endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Generate HTML content with links to each endpoint
    links_content = "".join(f"<li><a href='/{endpoint}'>{endpoint.capitalize()}</a></li>" for endpoint in endpoints_content.keys())
    html_content = f"<html><body><h1>Welcome to My Website!</h1><ul>{links_content}</ul></body></html>"
    return html_content

# Define endpoints for each category
#Sri's card section
@app.get("/hearthstone", response_class=HTMLResponse)
async def get_hearthstone_content():
    with open("Sri_web.html", "r") as file:
        html_content = file.read()
    return html_content

# Daniel's Food section
@app.get("/food", response_class=HTMLResponse)
async def get_food_content(request: Request):
    # Your HTML content for the food page
    html_content = """
        <html>
            <head>
                <title>Recipe Search</title>
                <style>
                    body {
                        background-color: #73A9AD; /* Set background color */
                        text-align: center; /* Center justify text */
                        display: flex; /* Use flexbox for centering */
                        align-items: center; /* Center vertically */
                        justify-content: center; /* Center horizontally */
                        height: 100vh; /* Set height to full viewport height */
                        margin: 0; /* Remove default margin */
                    }
                    h1 {
                        color: #B3C890; /* Set header color */
                        font-size: 60px; /* Increase header size */
                    }
                    form {
                        width: 50%; /* Set the form width */
                    }
                    label {
                        color: #B3C890; /* Set label color */
                        font-size: 20px; /* Increase header size */
                        display: block; /* Convert label to block element */
                        margin-bottom: 10px; /* Add space */
                    }
                    input[type="text"] {
                        width: 70%; /* Make search bar longer */
                    }
                </style>
            </head>
            <body>
                <h1>Recipe Search</h1>
                <form action="/search/" method="get">
                    <label for="query">Enter your topic:</label>
                    <input type="text" id="query" name="query"><br><br>
                    <input type="submit" value="Search">
                </form>
                <h1>Good Food Graphs</h1>
                <form action="/visualize/" method="get">
                    <label for="website">Enter website URL:</label>
                    <input type="text" id="website" name="website"><br><br>
                    <input type="submit" value="Visualize">
                </form>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)

templates = Jinja2Templates(directory="templates")  # Directory where your HTML templates are stored

RAPIDAPI_KEY = "5b09acfd1cmshc5f4874796c6823p1bbd93jsn896e7d8c7dce"
RAPIDAPI_HOST = "food-recipes-with-images.p.rapidapi.com"

def get_recipe(query: str):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': RAPIDAPI_HOST
    }
    conn.request("GET", f"/?q={query}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Function to extract categories from the provided URL
def extract_categories(url):
    try:
        # Make a request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the container that holds the categories
        container = soup.find('ul', class_='terms-icons-list')

        # Extract categories if the container is found
        if container:
            categories = [item.text.strip() for item in container.find_all('span', class_='terms-icons-list__text')]
            return categories
        else:
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract nutritional info from a recipe URL
def extract_nutritional_info(url):
    try:
        # Fetching the webpage content
        response = requests.get(url)

        # Checking if the request was successful
        if response.status_code == 200:
            # Extracting the HTML content of the webpage
            webpage_content = response.content

            # Parsing the HTML content using BeautifulSoup
            soup = BeautifulSoup(webpage_content, 'html.parser')

            # Find the script tag containing nutritionalInfo
            script_tags = soup.find_all('script', type='application/ld+json')

            for script in script_tags:
                script_content = script.string
                if script_content:
                    try:
                        # Parse JSON content
                        data = json.loads(script_content)

                        # Check if nutrition info exists in the JSON data
                        if 'nutrition' in data:
                            nutritional_info = data['nutrition']
                            protein_content_str = nutritional_info.get('proteinContent')
                            fat_content_str = nutritional_info.get('fatContent')
                            sodium_content_str = nutritional_info.get('sodiumContent')

                            # Convert string values to floats
                            protein_content = float(protein_content_str.split()[0])
                            fat_content = float(fat_content_str.split()[0])
                            sodium_content = float(sodium_content_str.split()[0])

                            return protein_content, fat_content, sodium_content
                    except (json.JSONDecodeError, ValueError):
                        pass  # Ignore if JSON parsing or conversion to float fails
        else:
            print("Failed to fetch the webpage. Status code:", response.status_code)
    except Exception as e:
        print("Error:", e)
    return None, None, None

@app.get("/search/", response_class=HTMLResponse)
async def search_recipe(request: Request, query: str):
    recipe_data = get_recipe(query)
    formatted_data = json.loads(recipe_data)

    # Extracting specific parts of the data
    results = formatted_data.get("d", [])
    formatted_results = []
    for result in results:
        formatted_result = {
            "Title": result.get("Title", ""),
            "Ingredients": result.get("Ingredients", {}),
            "Special Equipment": result.get("Ingredients", {}).get("14", ""),
            "Instructions": result.get("Instructions", "").replace("\n", "<br>"),
            "Image": result.get("Image", "")
        }
        formatted_results.append(formatted_result)

    return templates.TemplateResponse("recipe.html", {"request": request, "recipes": formatted_results})

@app.get("/visualize/", response_class=HTMLResponse)
async def visualize(request: Request, website: str):
    # Fetch all recipe links from the provided website
    webpage = requests.get(website)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    links = soup.find_all("article")

    # List to store all categories
    all_categories = []

    # Iterate through each recipe link
    for ele in links:
        recipe_url = 'https://www.bbcgoodfood.com' + ele.a["href"]

        # Extract categories for each recipe URL
        categories = extract_categories(recipe_url)

        # Add categories to the list
        if categories:
            all_categories.extend(categories)

    # Count the frequency of each category
    category_counter = Counter(all_categories)

    # Plotting the pie chart and box plot side by side
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Pie chart
    axes[0].pie(category_counter.values(), labels=category_counter.keys(), autopct='%1.1f%%', startangle=140)
    axes[0].set_title('Frequency of Categories')
    axes[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Box plot
    protein_values = []
    fat_values = []
    sodium_values = []

    # Iterate through each recipe link (limit to 10 for demonstration)
    for ele in links[:10]:
        recipe_url = 'https://www.bbcgoodfood.com' + ele.a["href"]

        # Extract nutritional info for each recipe
        protein_content, fat_content, sodium_content = extract_nutritional_info(recipe_url)

        # Add nutritional values to the lists if they are not None
        if protein_content is not None:
            protein_values.append(protein_content)
        if fat_content is not None:
            fat_values.append(fat_content)
        if sodium_content is not None:
            sodium_values.append(sodium_content)

    # Plot box plot
    axes[1].boxplot([protein_values, fat_values, sodium_values], labels=['Protein Content', 'Fat Content', 'Sodium Content'])
    axes[1].set_xlabel('Nutritional Content')
    axes[1].set_ylabel('Value (g)')
    axes[1].set_title('Protein, Fat and Sodium Content')

    # Convert the plot to a base64 encoded image
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.getvalue()).decode()

    # Embed the base64 image directly into the HTML response
    html_content = f"""
    <html>
        <head>
            <title>Visualization</title>
        </head>
        <body>
            <h1>Visualization</h1>
            <img src="data:image/png;base64,{img_base64}" alt="Pie Chart and Box Plot">
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

#Joanne's movies
@app.get("/movies")
async def read_root():
    html_content = """
    <html>
        <head>
            <title>Movie Search</title>
            <style>
                body {
                    background-color: #f0f0f0;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                h1 {
                    color: #333333;
                }
                form {
                    margin-top: 20px;
                }
                input[type="text"] {
                    padding: 8px;
                    width: 300px;
                }
                input[type="submit"] {
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                .button-container {
                    margin-top: 20px;
                }
                .button-container button {
                    margin: 0 10px;
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <h1>Movie Search</h1>
            <form action="/get/movies" method="get">
                <label for="title">Enter movie title:</label>
                <input type="text" id="title" name="title">
                <input type="submit" value="Search">
            </form>
            <div class="button-container">
                <button onclick="location.href='/get/popular/movies/1'">Popular Movies</button>
                <button onclick="location.href='/get/nowplaying/movies/1'">Now Playing</button>
                <button onclick="location.href='/get/upcoming/movies/1'">Upcoming Movies</button>
            </div>
            <form action="/get/movies/year" method="get">
                <label for="year">Enter year:</label>
                <input type="text" id="year" name="year">
                <input type="submit" value="Search">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/get/movies/{title}")
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

@app.get("/get/popular/movies/{page}")
async def get_popular_movies(page: str):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"page": page}  # Assuming you want to start at page 1
    headers = {
        "Type": "get-popular-movies",
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return JSONResponse(content=response.json())

@app.get("/get/nowplaying/movies/{year}")
async def get_nowplaying_movies(page: str):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"page":"1"}
    headers = {
        "Type": "get-nowplaying-movies",
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return JSONResponse(content=response.json())

@app.get("/get/upcoming/movies/{page}")
async def get_upcoming_movies(page: str):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"page": page}  # Assuming you want to start at page 1
    headers = {
        "Type": "get-upcoming-movies",
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return JSONResponse(content=response.json())

@app.get("/get/movies/year/{year}")
async def get_movies_by_year(year: str):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"year": year, "page": "1"}  # Assuming you want to start at page 1
    headers = {
        "Type": "get-movies-byyear",
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return JSONResponse(content=response.json())

#Wang's books
@app.get("/books", response_class=HTMLResponse)
async def get_hearthstone_content():
    with open("templates/homepage.html", "r") as file:
        html_content2 = file.read()
    return html_content2

#Julie's show site:
# Define route for the new "shows website" endpoint
@app.get("/shows", response_class=HTMLResponse)
async def shows_website():
    # Redirect to the specified website
    return HTMLResponse(content="<script>window.location.href='https://cajulie.pythonanywhere.com/';</script>")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)