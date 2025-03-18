from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from readability import Document
from langdetect import detect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
import os
import spacy

nltk.download('punkt')  # Pentru tokenizare
nltk.download('punkt_tab')
nltk.download('stopwords')  # Pentru stopwords în diverse limbi

load_dotenv()

app = FastAPI()


class NewsInput(BaseModel):
    url: str

@app.get("/extract_text")
def extract_text(url: str):
    page = requests.get(url)
    if page.status_code == 200:

        doc = Document(page.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")

        title = doc.title()

        for tag in soup(["script", "style", "aside", "nav"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        try:
            lang = detect(text)
        except:
            lang = "unknown"

        return {"title": title ,"text": text, "language": lang}
    
    else:

        return {"error": "URL not accessible"}

def extract_key_words(text: str, language: str):
    try:
        stop_words = set(stopwords.words(language))
    except:
        stop_words = set()

    words = word_tokenize(text)
    keywords = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    
    return " ".join(keywords[:5])

# def extract_key_words_spacy(text: str, language: str):
#     nlp = spacy.load(language)
#     doc = nlp(text)

#     keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
    
#     return keywords

def search_newsapi(query: str, language: str, num_results: int = 20):
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

    url = "https://newsapi.org/v2/everything"

    refined_query = extract_key_words(query, language)
    
    params = {
        "q": refined_query,
        "language": language,
        "pageSize": num_results,
        "sortBy": "relevancy",
        "apiKey": NEWSAPI_KEY,
    }

    response = requests.get(url, params=params)

    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [{"keywords": refined_query ,"title": article["title"], "url": article["url"]} for article in articles]
    else:
        return {"error": "NewsAPI request failed"}

def extract_text_helper(url: str):
    return extract_text(url)

def search_google(query: str, language: str, num_results: int = 10):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

    keywords = extract_key_words(query, language)

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": keywords,  # Cuvinte cheie
        "cx": GOOGLE_CSE_ID,  # Custom Search Engine ID
        "key": GOOGLE_API_KEY,  # API Key
        "lr": f"lang_{language}",  # Limba căutării
        "num": num_results,  # Numărul de rezultate
    }

    response = requests.get(url, params=params)

    # print(f"Request URL: {response.url}")
    # print(f"Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")

    if response.status_code == 200:
        search_results = response.json()
        return [{"keywords": keywords, "title": item["title"], "link": item["link"]} for item in search_results.get("items", [])]
    else:
        return {"error": "Google Custom Search API request failed"}


@app.get("/related_news")
def related_news(url: str):
    extracted_data = extract_text_helper(url)

    if "error" in extracted_data:
        return extracted_data
    
    title = extracted_data["title"]
    language = extracted_data["language"]

    newsapi_results = search_newsapi(title, language)
    google_results = search_google(title, language)

    return {
        "title": title,
        "language": language,
        "newsapi_related_news": newsapi_results,
        "google_related_news": google_results
    }

@app.post("/check_factuality")
def check_factuality(news_input: NewsInput):
    return {"message": f"Received URL: {news_input.url}"}