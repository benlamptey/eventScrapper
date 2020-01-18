import requests
import json
import sys
from bs4 import BeautifulSoup

data = ['event', 'date', 'time']
URL = 'https://www.tottenhamhotspur.com/the-stadium/events/stadium-events/'
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0'}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

eventTable = soup.find("table")
body_table = eventTable.find('tbody')
rows = body_table.find_all('tr')


def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")

    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.find_all("td")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower().replace(' ', '_')
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            for index in headers:
                items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        data.append(items)
        # remove the headers. its coming up as first element for some reason.

    data.pop(0)
    formattedList = {}
    formattedList['nextEvent'] = data[1]
    formattedList['upcomingEvents'] = data
    formattedList['upcomingEvents'].pop(0)
    return json.dumps(formattedList, indent=indent)


events = html_to_json(page.content, indent=2)

f = open(sys.argv[1], "w")
f.write(events)
f.close()