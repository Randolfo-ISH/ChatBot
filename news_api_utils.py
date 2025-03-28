import requests

def get_news(category, query=None, language='pt', country='br', api_key="SUA_CHAVE_DE_API_NEWSAPI"):
    """
    Busca notícias usando a API do NewsAPI.org.

    Args:
        category (str): A categoria das notícias (e.g., "technology", "business").
        query (str, optional): Palavra-chave para refinar a busca. Defaults to None.
        language (str, optional): O idioma das notícias. Defaults to 'pt'.
        country (str, optional): O país das notícias. Defaults to 'br'.
        api_key (str): Sua chave de API do NewsAPI.org.

    Returns:
        list: Uma lista de artigos de notícias (dicionários) com título, fonte e descrição.
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'category': category,
        'language': language,
        'country': country,
        'apiKey': api_key
    }
    if query:
        params['q'] = query

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = []
        for article in data.get('articles', []):
            articles.append({
                'title': article.get('title'),
                'source': article['source'].get('name'),
                'description': article.get('description') or article.get('content') or article.get('url') # Pega description, content ou url como fallback
            })
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar notícias de {category}: {e}")
        return []