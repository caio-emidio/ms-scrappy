import requests
from bs4 import BeautifulSoup


def montaImg(time):
    return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/{time}.png"

def trataTeam(teams, resultado, index):
    homeId = teams[index]["href"].split("/")[5]

    result = {
        "name": teams[index].text,
        "image": montaImg(homeId),
        "score": resultado[index],
    }

    return result

def trataTabelaResultado(tabela):
    dia = tabela.find_all('div', {'class': 'matchTeams'})
    teams = tabela.find_all('a', {'class': 'AnchorLink Table__Team'})
    tdTable = tabela.find_all('td', {'class': 'Table__TD'})
    homeId = teams[0]["href"].split("/")[5]
    awayId = teams[1]["href"].split("/")[5]
    infoMatch = tdTable[2].find_all('a', {'class': 'AnchorLink'})
    resultado = infoMatch[1].text.replace(" ","").split("-")

    result = {
        "data": dia[0].text.split(",")[1].strip().split(".")[0].replace(" ", "/"),
        "home": trataTeam(teams, resultado, 0),
        "away": trataTeam(teams, resultado, 1),
        "championship": tdTable[5].text,
    }

    return result


def trataTabelaCalendario(tabela):
    dia = tabela.find_all('div', {'class': 'matchTeams'})
    teams = tabela.find_all('a', {'class': 'AnchorLink Table__Team'})
    tdTable = tabela.find_all('td', {'class': 'Table__TD'})
    homeId = teams[0]["href"].split("/")[5]
    awayId = teams[1]["href"].split("/")[5]

    result = {
        "data": dia[0].text.split(",")[1].strip().split(".")[0].replace(" ", "/"),
        "time": tdTable[4].text,
        "home": teams[0].text,
        "homeImg": montaImg(homeId),
        "away": teams[1].text,
        "awayImg": montaImg(awayId),
        "championship": tdTable[5].text,
    }

    return result


def result(url):
    result = []
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')

    filmes = soup.find_all('div', {'class': 'ItemN'})
    result = []
    for filme in filmes:
        result.append(trata_filme(filme))
    return {"data": result}


def busca(tipo):
    url = f"https://www.espn.com.br/futebol/time/{tipo}/_/id/3458"
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    allTables = soup.find_all(
        'tr', {'class': 'Table__TR Table__TR--sm Table__even'})
    result = []

    if(tipo == "calendario"):
        for table in allTables:
            result.append(trataTabelaCalendario(table))
        return result

    if(tipo == "resultados"):
        for table in allTables:
            result.append(trataTabelaResultado(table))
        return result
    return result
