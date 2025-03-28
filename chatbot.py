import os
import google.generativeai as genai
import textwrap
import time
import news_api_utils
from dotenv import load_dotenv
from IPython.display import display, Markdown
from typing import List, Dict

import requests

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
API_KEY = os.getenv("API_NEWSAPI")

def get_news(category, query=None, language='pt', country='br'):
    """
    Busca notícias usando a API do NewsAPI.org.

    Args:
        category (str): A categoria das notícias (e.g., "technology", "business").
        query (str, optional): Palavra-chave para refinar a busca. Defaults to None.
        language (str, optional): O idioma das notícias. Defaults to 'pt'.
        country (str, optional): O país das notícias. Defaults to 'br'.

    Returns:
        list: Uma lista de artigos de notícias (dicionários).
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'category': category,
        'language': language,
        'country': country,
        'apiKey': API_KEY
    }
    if query:
        params['q'] = query

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Lança uma exceção para códigos de status ruins
        data = response.json()
        return data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar notícias de {category}: {e}")
        return []

if __name__ == "__main__":
    if API_KEY == "SUA_CHAVE_DE_API_NEWSAPI":
        print("Por favor, substitua 'SUA_CHAVE_DE_API_NEWSAPI' pela sua chave de API real do NewsAPI.org.")
    else:
        print("Buscando notícias de tecnologia sobre temas atuais:")
        technology_topics = ["Inteligência Artificial", "Cybersegurança", "Computação em Nuvem", "Veículos Elétricos", "Metaverso", "Blockchain"]
        for topic in technology_topics:
            print(f"\n--- Notícias sobre: {topic} ---")
            articles = get_news(category='technology', query=topic)
            if articles:
                for article in articles:
                    print(f"  Título: {article['title']}")
                    print(f"  Fonte: {article['source']['name']}")
                    print(f"  URL: {article['url']}")
                    print("-" * 40)
            else:
                print("  Nenhuma notícia encontrada.")

        print("\nBuscando notícias de negócios sobre temas atuais:")
        business_topics = ["Inteligência Artificial", "Transformação Digital", "ESG", "Mercado de Criptomoedas", "E-commerce", "Trabalho Remoto"]
        for topic in business_topics:
            print(f"\n--- Notícias sobre: {topic} ---")
            articles = get_news(category='business', query=topic)
            if articles:
                for article in articles:
                    print(f"  Título: {article['title']}")
                    print(f"  Fonte: {article['source']['name']}")
                    print(f"  URL: {article['url']}")
                    print("-" * 40)
            else:
                print("  Nenhuma notícia encontrada.")
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

if not GOOGLE_API_KEY:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Use a ferramenta de busca para obter notícias recentes
search_queries = ["recent data technology news", "últimas notícias tecnologia de dados", "tendências recentes ciência de dados e análise"]
all_results: List[Dict] = []
news_count = 0
max_news = 20

for i, query in enumerate(search_queries):
    if news_count >= max_news:
        print("Limite de 20 notícias atingido. Interrompendo buscas.")
        break

    print(f"Realizando busca para: {query}")
    try:
        search_response = GoogleSearch(queries=[query])
        for result in search_response:
            if 'results' in result:
                for item in result['results']:
                    if news_count < max_news:
                        all_results.append(item)
                        news_count += 1
                    else:
                        print("Limite de 20 notícias atingido. Interrompendo processamento de resultados.")
                        break
            if news_count >= max_news:
                break

    except Exception as e:
        print(f"Erro durante a busca para '{query}': {e}")

    if i < len(search_queries) - 1:  # Adiciona um delay se não for a última busca
        print("Aguardando 1 segundo antes da próxima busca...")
        time.sleep(1)

# Extrai os snippets das notícias
news_snippets = []
for result in all_results:
    if 'snippet' in result and result['snippet']:
        news_snippets.append(result['snippet'])

# Se não encontrarmos nenhum snippet, podemos usar os títulos como fallback
if not news_snippets and all_results:
    for result in all_results:
        if 'title' in result and result['title']:
            news_snippets.append(result['title'])

if not news_snippets:
    print("Nenhuma notícia relevante encontrada.")
else:
    # Crie um prompt para o Gemini resumir as notícias em português
    prompt = f"""Por favor, forneça um breve resumo em português das seguintes notícias e tendências no mundo da tecnologia de dados:

{news_snippets}

Mantenha o resumo conciso e destaque os principais desenvolvimentos."""

    # Envie o prompt para o modelo Gemini
    try:
        response = model.generate_content(prompt)

        # Exiba a resposta em português
        if response.parts:
            text_response = response.parts[0].text
            print("Resumo das Notícias de Tecnologia de Dados (em Português):")
            display(to_markdown(text_response))
        else:
            print("Nenhuma resposta de texto foi recebida.")
    except Exception as e:
        print(f"Erro ao gerar conteúdo com o Gemini: {e}")