from bs4 import BeautifulSoup
import re
import time
import Messages
from random import randint


class Build:
    def __init__(self, session, url, debug=False):
        self.session = session
        self.debug = debug
        self.url = url + '/dorf1.php'

    def resources(self, soup):
        '''funkcia na ziskanie momentalneho stavu surovin v podobe dict'''
        res = soup.find_all('span', {'class': 'value'})
        resources = {"drevo": (res[1].contents[0]), "hlina": res[2].contents[0],
                     "zelezo": res[3].contents[0], "obilie": res[5].contents[0]}

        for k, v in resources.items():
            resources[k] = re.search(r'\b\d+\b', v).group(0)
        return resources

    def get_soup(self, url=None):
        if url is None:
            return BeautifulSoup(self.session.get(self.url).content,
                                 'html.parser')
        if self.debug:
            print(url)
        return BeautifulSoup(self.session.get(url).content, 'html.parser')

    def build(self):
        chosen_one = self.lowest_resource_build(self.get_soup())
        soup = self.get_soup('https://ts3.travian.cz/build.php?id=' +\
                             str(chosen_one))
        temp = soup.find('button', {'class': 'green build'})  # ziska link postavania budovy
        self.session.post('https://ts3.travian.cz/' + temp['onclick'].split("'")[1])


    def lowest_resource_build(self, soup):
        '''funkcia ktora vrati id policka typu suroviny, ktorej je najmenej a najnizsieho lvlu '''
        enum = {'drevo': [0, 2, 13, 16], 'hlina': [4, 5, 15, 17],
                'zelezo': [3, 6, 9, 10], 'obilie': [1, 7, 8, 11, 12, 14]}
        res = self.resources(soup)
        min_res = str(min(res, key=lambda x: res[x]))
        if self.debug:
            print(res)
        lvls = []
        for each in soup.find_all('area'):
            lvls += each.get('alt')
        lvls = [x for x in lvls if x.isdigit()]
        chosen_one = int(enum[min_res][0])
        for x in enum[min_res]:
            if int(lvls[x]) < int(lvls[chosen_one]):
                chosen_one = int(x)
        if self.debug:
            print("building " + min_res + ", id=" + str(chosen_one + 1))
        return chosen_one+1


    def repetitive_build(session, min):
        '''funkcia ktora vola stavanie kazdych +-in_min minut'''
        for x in range(10):
            in_secs = rando(min)
            Messages.build_at(in_secs)
            time.sleep(in_secs)
            self.build()


    def build_in(self, h, m, s):
        delay = (h*60 + m)*60+s
        Messages.build_at(delay)
        time.sleep(delay)
        self.build()


def rando(min):
    '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
    rand_secs = abs((randint((min-2)*100, (min+2)*100) / 100)*60)
    return rand_secs
