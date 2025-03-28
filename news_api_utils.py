import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_NEWSAPI = os.getenv("API_NEWSAPI")

def get_news(category, api_key):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}"
    print(url)
    headers = {'User-Agent': 'MeuAplicativo/1.0'}  # Substitua por algo mais descritivo
    response = requests.get(url, headers=headers)
    return response.json()

news_data = get_news("technology", API_NEWSAPI)