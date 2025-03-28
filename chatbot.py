import os
import google.generativeai as genai
import textwrap
import time
import news_api_utils as news
from dotenv import load_dotenv
from IPython.display import display, Markdown
from typing import List, Dict

import requests

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NEWS_API_KEY = os.getenv("API_NEWSAPI")

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

if not GOOGLE_API_KEY:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    exit()

if not NEWS_API_KEY:
    print("Erro: A variável de ambiente NEWS_API_KEY não está configurada.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Use a ferramenta de busca para obter notícias recentes
search_queries = ["recent data technology news", "últimas notícias tecnologia", "tendências recentes ciência de dados e análise"]
all_results: List[Dict] = []
news_count = 0
max_news = 20
category = "technology"

for i, query in enumerate(search_queries):
    if news_count >= max_news:
        print("Limite de 20 notícias atingido. Interrompendo buscas.")
        break

    print(f"Realizando busca para: {query}")
    try:
        search_response = news.get_news(category=category, query=query, api_key=NEWS_API_KEY)
        for item in search_response:
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
    if 'description' in result and result['description']:
        news_snippets.append(result['description'])

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