import travianBot
from bs4 import BeautifulSoup


def get_adventures(session, url):
    adventures = []
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('form', attrs={'id':'adventureListForm'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        test = row.find_all('td')
        a = test[2].renderContents()
        a = str(a)
        adventures.append([a[18:25], row['id'][9:]])
    return adventures

def go_on_adventure(session, id_dobrodruzstva, url):
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    button = soup.find("button", {"class": "green "})
    url = url + "/start_adventure.php?from=list&kid=" + id_dobrodruzstva
    print(url)
    session.post(url, {"value":"Jít na výpravu"})

def get_hero_status(session, url):
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('div', attrs={'class':'heroStatusMessage'})
    print(table.renderContents())

travian = travianBot.Travian("Scasike", "firebrand")
adventures = get_adventures(travian.session, "https://ts1.travian.cz/hero.php?t=3")
go_on_adventure(travian.session, adventures[0][1], "https://ts1.travian.cz")
