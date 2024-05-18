import requests
from bs4 import BeautifulSoup
import json

def busca(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    main = soup.find('div', {"data-testid": "mainContent"})
    date = main.find('time', {"class": "start-date"})
    title = main.find('h1', {"class": "event-title"})
    location = main.find('p', {"class": "location-info__address-text"})

    ownerRegion = soup.find('section', {"aria-label": "Organizer profile"})

    owner = ownerRegion.find('strong')

    imgRegion = soup.find('picture', {"data-testid":"hero-image"})
    img = imgRegion.find('img')
    img_src = img.get('src')


    data = {
        "title": title.text.title(),
        "date": date.attrs['datetime'],
        "url": url,
        "location": location.text,
        "owner": owner.text,
        "img": img_src
    }
    

    addPage(data)

    return data


def addPage(data):
    payload = json.dumps({
        "parent": {
            "database_id": "1335fbda0a0b4dce9e330224ae40a6d3"
        },
        "icon": {
            "emoji": "🚩"
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": data['title']
                        }
                    }
                ]
            },
            "Owner": {
                "select": {
                    "name": data['owner']
                }
            },
            "Date": {
                "date": {
                    "start": data['date']
                }
            },
            "Location": {
                "select": {
                    "name": data['location']
                }
            },
            "City": {
                "multi_select": [{
                    "name": "Dublin"
                }]
            },
            "URL": {
                "url": data['url']
            },
            "Photo": {
                "type": "files",
                "files": [
                    {
                        "name": data['title'] + " Image",
                        "type": "external",
                        "external": {
                            "url": data['img']
                        }
                    }
                ]
            }
        }
    })
    headers = {
    'Authorization': 'Bearer secret_2VdrsG2w6aBuALQB1JW1aOp7GvY6rX8XMYb1riAiHPz',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
    }

    url = "https://api.notion.com/v1/pages"

    response = requests.request("POST", url, headers=headers, data=payload)