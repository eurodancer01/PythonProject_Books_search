from flask import Flask, jsonify, request
import requests
from fastapi import HTTPException,Query
import requests
from typing import List

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Book Finder API</h1>
    <p>Use our API to find books by ID, author, genres, rating, and title.</p>
    <ul>
        <li><a href="/books/6">Find a Book by ID</a></li>
        <li><a href="/find_book_by_author?lname=Dickens&fname=Charles">Find Books by Author</a></li>
        <li><a href="/find_books_by_genres/genres=fantasy">Find Books by Genres</a></li>
        <li><a href="/find_books_by_rating?lte=5&gte=1&p=1">Find Books by Rating</a></li>
        <li><a href="/find_book_by_title?title=Example">Find a Book by Title</a></li>
    </ul>
    '''

@app.route('/books/<int:book_id>')
def get_book_by_id(book_id):
    url = f"https://books-api7.p.rapidapi.com/books/{book_id}"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))# Implementation of the API call as shown in your FastAPI app
    return jsonify({"message": "Book information for ID " + str(book_id)})

@app.route('/find_book_by_author')
def find_book_by_author():
    lname = request.args.get('lname', '')  # Default to empty string if not provided
    fname = request.args.get('fname', '')  # Default to empty string if not provided

    # Ensure both first name and last name are provided
    if not lname or not fname:
        return jsonify({"error": "Both first name (fname) and last name (lname) are required."}), 400

    url = "https://books-api7.p.rapidapi.com/books/find/author"
    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace YOUR_RAPIDAPI_KEY with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"lname": lname, "fname": fname}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.HTTPError as http_err:
        return jsonify({"error": "HTTPError occurred", "details": str(http_err)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/find_books_by_genres')
def find_books_by_genres():
    genres = request.args.getlist('genres')  # Extract genres from query parameters
    if not genres:
        genres = ["fantasy"]  # Default genre if none provided
    
    url = "https://books-api7.p.rapidapi.com/books/find/genres"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",  # Replace YOUR_RAPIDAPI_KEY with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"genres[]": genres}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.HTTPError as http_err:
        return jsonify({"error": "HTTPError occurred", "details": str(http_err)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    
@app.route('/find_books_by_rating')
def find_books_by_rating():
    lte = request.args.get('lte', '')  # Rating less than or equal to
    gte = request.args.get('gte', '')  # Rating greater than or equal to
    p = request.args.get('p', '1')  # Page number, defaulting to 1

    url = "https://books-api7.p.rapidapi.com/books/find/rating"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",  # Replace with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"lte": lte, "gte": gte, "p": p}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.HTTPError as http_err:
        return jsonify({"error": "HTTPError occurred", "details": str(http_err)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/find_book_by_title')
def find_book_by_title():
    title = request.args.get('title', '')  # Title of the book

    url = "https://books-api7.p.rapidapi.com/books/find/title"
    headers = {
        "X-RapidAPI-Key": "b722b31fb0msh08be9a4691d2d07p119105jsnb6ca8bbdbb53",  # Replace YOUR_RAPIDAPI_KEY with your actual API key
        "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
    }
    params = {"title": title}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return jsonify(response.json())
    except requests.HTTPError as http_err:
        return jsonify({"error": "HTTPError occurred", "details": str(http_err)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
