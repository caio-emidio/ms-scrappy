import requests
from bs4 import BeautifulSoup
import datetime

def convert_timezone(data, znOrigem, znDestino):
    from zoneinfo import ZoneInfo
    from datetime import datetime

    d = datetime(data["year"], data["month"], data["day"], data["hour"], data["minute"], tzinfo=ZoneInfo(znOrigem))
    return d.astimezone(ZoneInfo(znDestino)).strftime("%d/%m/%Y %H:%M")

def montaImg(time):
    return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/{time}.png"

def trataTeam(teams, resultado, index):
    homeId = teams[index]["href"].split("/")[5]

    result = {
        "name": teams[index].text,
        "image": montaImg(homeId),
    }

    if(len(resultado) > 0):
        result["score"] = resultado[index]

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

def trata_mes(mes):
    if mes == "jan":
        return 1
    if mes == "fev":
        return 2
    if mes == "mar":
        return 3
    if mes == "apr":
        return 4
    if mes == "mai":
        return 5
    if mes == "jun":
        return 6
    if mes == "jul":
        return 7
    if mes == "ago":
        return 8
    if mes == "set":
        return 9
    if mes == "out":
        return 10
    if mes == "nov":
        return 11
    if mes == "dec":
        return 12


def trataTabelaCalendario(tabela):
    dia = tabela.find_all('div', {'class': 'matchTeams'})
    teams = tabela.find_all('a', {'class': 'AnchorLink Table__Team'})
    tdTable = tabela.find_all('td', {'class': 'Table__TD'})

    tratadoDia = dia[0].text.split(",")[1].strip().split(".")[0].replace(" ", "/")
    diaCerto = tratadoDia.split("/")[0]
    mesCerto = trata_mes(tratadoDia.split("/")[1])
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    anoCerto = date.strftime("%Y")
    horario = tdTable[4].text
    resultadoDia = dia[0].text.split(",")[1].strip().split(".")[0].replace(" ", "/")
    resultadoTime = tdTable[4].text
    if horario != "A definir":
        horario = resultadoTime.split(":")
        dataCorreta = {
            "year": int(anoCerto),
            "month": mesCerto,
            "day": int(diaCerto),
            "hour": int(horario[0]),
            "minute": int(horario[1]),
        }
        resultado = convert_timezone(dataCorreta, 'America/New_York', "Europe/Dublin").split(" ")
        resultadoDia = resultado[0]
        resultadoTime = resultado[1]

    result = {
        "data": resultadoDia,
        "time": resultadoTime,
        "home": trataTeam(teams, [], 0),
        "away": trataTeam(teams, [], 1),
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
