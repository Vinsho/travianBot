import travianBot
from bs4 import BeautifulSoup

class Hero:
    def __init__(self, session, url, debug=False):
        self.session = session
        self.url = url + '/hero.php'
        self.debug = debug

    def get_soup(self, url=None):
        if url is None:
            return BeautifulSoup(self.session.get(self.url).content,
                                 'html.parser')
        return BeautifulSoup(self.session.get(url).content, 'html.parser')

    def get_adventures(self):
        adventures = []
        soup = self.get_soup(self.url+'?t=3')
        table = soup.find('form', {'id':'adventureListForm'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            udaje = row.find_all('td')
            adventures.append([udaje[0].text.strip(), udaje[2].text.strip(),
                               udaje[3].find('img', alt=True)['alt'],
                               udaje[4].text.strip(), row['id'][9:]])
        return adventures

    def go_on_adventure(self, id_dobrodruzstva):
        url = self.url[:-8] + "start_adventure.php?from=list&kid=" +\
              id_dobrodruzstva
        self.session.post(url, {'value': 'Jít na výpravu', 'send' : '1',
                                'kid' : id_dobrodruzstva, 'a':'1',
                                'from':'list'})

    def get_hero_status(self):
        table = self.get_soup().find('div', attrs={'class':'heroStatusMessage'})
        return table.text.strip()

def get_first_adventure_to_expire_id(adventures):
    ad_times = [(x[4], x[3].split(":")) for i, x in enumerate(adventures)]
    for i, time in enumerate(ad_times):
        ad_times[i] = time[0], int(time[1][0])*3600 + int(time[1][1])*60 + int(time[1][2])
    minimum = ad_times[0][1]
    minimum_id = ad_times[0][0]
    for i, time in enumerate(ad_times):
        if time[1] < minimum:
            minimum, minimum_id = time, time[0]
    return minimum_id

if __name__ == "__main__":
    travian = travianBot.Travian("Scasike", "firebrand", 'https://ts3.travian.cz')
    adventures = get_adventures(travian.session, "https://ts3.travian.cz/hero.php?t=3")
    id_a = get_first_adventure_to_expire_id(adventures)
    print(id_a)
    go_on_adventure(travian.session, id_a, travian.url)
