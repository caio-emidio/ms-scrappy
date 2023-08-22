import requests
from bs4 import BeautifulSoup


def trata_filme(filme):
    poster = filme.find('div', {'class': 'box-filme-img'})
    link = filme.find('a', {'class': 'filme-link'})
    return {
        "name": poster.find('img')["alt"],
        "url": link['href'],
        "img": poster.find('img')["src"]
    }


def result(url):
    result = []
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')

    filmes = soup.find_all('div', {'class': 'box-filme-container'})
    
    result = []
    print(filmes[0])
    for filme in filmes:
        result.append(trata_filme(filme))
    return result

def detalhes_filme(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    div_links = soup.find_all('a', {'style': 'color: #fff;'})
    
    result = []
    for link in div_links:
        result.append({"name": link.text, "url": link['href'].split('&')[0]})
    return {"data": result}