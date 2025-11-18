import requests
import random
import json  
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

OPEN_LIBRARY_URL = "https://openlibrary.org"

def get_book_by_theme(theme: str) -> str: 
    """
    Fetches a random book from the Open Library API based on a subject/theme.
    
    Args:
        theme: The theme (e.g., "identity", "historical fiction").

    Returns:
        A JSON string with book details (title, author, subjects)
        or a plain string message if no books are found.
    """
    formatted_theme = theme.lower().replace(" ", "_")
    url = f"{OPEN_LIBRARY_URL}/subjects/{formatted_theme}.json?limit=50"
    print(f"🕵️  Searching for books about: '{theme}' at {url}...")

    try:
        data = requests.get(url).json()
        works = data.get("works")
        if not works:
            print(f"Sorry, I couldn't find any books for the theme '{theme}'.")
            return f"Sorry, no books were found for the theme '{theme}'." 

        book = random.choice(works)
        title = book.get("title", "Unknown Title")
        authors = book.get("authors", [])
        author = authors[0].get("name", "Unknown Author") if authors else "Unknown Author"
        subjects = book.get("subject", [])[:5]

        details = {
            "title": title,
            "author": author,
            "subjects": subjects
        }
        print(f"Found book: {details}")
        return json.dumps(details)

    except Exception as e:
        print(f"API Error: {e}")
        return f"An error occurred while searching for books: {e}"

openai_backed_model = LiteLlm(model="openai/gpt-4o")

root_agent = LlmAgent(
    name="book_recommendation_agent",
    model=openai_backed_model,
    instruction=(
        "You are a helpful assistant that can find books for a user. "
        "Call the get_book_by_theme tool. This tool returns a JSON string "
        "with the book details, or a plain string error message. "
        "If you get JSON, parse it and present the details nicely. "
        "If you get a plain string, just repeat that message to the user."
    ),
    description=(
        "A demo agent that uses the Open Library API to find a book by a theme."
    ),
    tools=[
        get_book_by_theme
    ],
)