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
        self.dorf2_url = url + '/dorf2.php'
        self.build_url = url + '/build.php?id='
        self.statictics_url = url + "/statistiken.php"

    def resources(self):
        '''funkcia na ziskanie momentalneho stavu surovin v podobe dict'''
        soup = self.get_soup(self.url)
        res = soup.find_all('span', {'class': 'value'})
        resources = {"Dřevo": (res[1].contents[0]), "Hlína": res[2].contents[0],
                     "Železo": res[3].contents[0], "Obilí": res[5].contents[0]}

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

    def upgrade(self, chosen_one):
        soup = self.get_soup(self.build_url + str(chosen_one))
        temp = soup.find('button', {'class': 'green build'})  # ziska link postavania budovy
        self.session.post(self.url[:-9] + temp['onclick'].split("'")[1])

    def build(self, building):
        '''pokial sa jedna o pole da upgradovat najnizsi lvl jeho typu,
           pokial je uz budova postavena, da ju upgradovat, ked nie da ju stavat.
        '''
        if any (building == x for x in self.resources().keys()):
            self.upgrade(self.get_id_of_lowest_res_lvl(building))
        elif self.is_building_built(building) != -1:
            self.upgrade(self.get_building_id(building))
        else:
            soup = self.get_soup(self.build_url + self.get_free_building_place_id())
            divs = soup.findAll('div', {'class': 'buildingWrapper'})
            for i in range(len(divs)):
                if divs[i].find('h2').string == building:
                    index = i
                    break
            button_link = divs[index].find('button', {'class': 'green new'})['onclick'].split("'")[1]
            self.session.post(self.url[:-9] + button_link)

    def get_lowest_resource_type(self):
        '''vrati surovinu ktorej je najmenej'''
        res = self.resources()
        min_res = str(min(res, key=lambda x: res[x]))
        return min_res

    def get_id_of_lowest_res_lvl(self, res):
        '''funkcia ktora vrati id policka typu suroviny, ktorej je najmenej a najnizsieho lvlu '''
        enum = {'Dřevo': [0, 2, 13, 16], 'Hlína': [4, 5, 15, 17],
                'Železo': [3, 6, 9, 10], 'Obilí': [1, 7, 8, 11, 12, 14]}
        soup = self.get_soup(self.url)
        lvls = []
        for each in soup.find_all('area'):
            lvls += each.get('alt')
        lvls = [x for x in lvls if x.isdigit()]  # ziska vsetky urovne policok
        chosen_one = int(enum[res][0])
        for x in enum[res]: # prejde vsetky policka min_res suroviny a zisti ktore ma najmensi lvl
            if int(lvls[x]) < int(lvls[chosen_one]):
                chosen_one = int(x)
        if self.debug:
            print("building " + res + ", id=" + str(chosen_one + 1))
        return chosen_one+1

    # def repetitive_build(self, min):
    #     '''funkcia ktora vola stavanie kazdych +-in_min minut'''
    #     for x in range(10):
    #         in_secs = self.rando(min)
    #         Messages.build_at(in_secs)
    #         time.sleep(in_secs)
    #         self.build_lowest()
    #
    # def build_in(self, h, m, s):
    #     delay = (h*60 + m)*60+s
    #     Messages.build_at(delay)
    #     time.sleep(delay)
    #     self.build_lowest()

    def get_pop(self):
        soup = self.get_soup(self.statictics_url)
        info = soup.find('tr', {'class': 'hl'})
        return int(info.find('td', {'class': 'pop'}).string)

    def get_production_per_hour(self):
        '''
            Vrati hodinovu produkciu dediny
            return: {'Surovina': mnozstvo}
        '''
        recourses = dict()
        soup = self.get_soup()
        table = soup.find('table', {'id':'production'})
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            num = int(tds[2].text.strip().encode('ascii', 'ignore'))
            recourses[tds[1].text.strip()[:-1]] = num
        return recourses

    def get_warehouse_capacity(self):
        soup = self.get_soup()
        capacity = float(soup.find('span', {'id': 'stockBarWarehouse'}).string.encode('ascii', 'ignore'))
        if capacity < 800:
            capacity *= 1000
        return capacity

    def get_granary_capacity(self):
        soup = self.get_soup()
        capacity = float(soup.find('span', {'id': 'stockBarGranary'}).string.encode('ascii', 'ignore'))
        if capacity < 800:
            capacity *= 1000
        return capacity

    def get_free_crop(self):
        soup = self.get_soup()
        free_crop = soup.find('span', {'id': 'stockBarFreeCrop'}).text.strip().encode('ascii', 'ignore')
        return int(free_crop)

    def get_free_building_place_id(self):
        soup = self.get_soup(self.dorf2_url)
        building_places = soup.findAll('area', {'alt': 'Staveniště'})
        return str(building_places[0]['href'].split('=')[1])

    def is_building_built(self, building):
        '''zisti ci je budova postavana, pokial ano vrati jej index(0 pre id=19), pokial nie vracia -1'''
        soup = self.get_soup(self.dorf2_url)
        areas = soup.findAll('area')
        areas = [a['alt'].split(" <")[0] for a in areas]
        for i in range(len(areas)):
            if building in areas[i]:
                return i
        else:
            return -1

    def get_building_lvl(self, building):
        '''vrati lvl budovy, pokial nie je postavena -1'''
        index = self.get_building_id(building)
        if index != -1:
            soup = self.get_soup(self.build_url + str(index))
            return int(soup.find('span', {'class':  'level'}).string.split(" ")[1])
        else:
            return -1

    def get_building_id(self, building):
        '''vrati id budovy, pokial nie je postavena vracia -1'''
        index = self.is_building_built(building)
        if index != -1:
            return index+19
        else:
            return -1

    def what_to_build(self):
        '''funkcia ktora vrati podla podmienok co sa ma dalej stavat'''
        pop = self.get_pop()
        if self.get_free_crop() < 5:
            return 'Obilí'
        if pop/15 > self.get_building_lvl('Hlavní budova'):  # kazdych 15 pop + 1 uroven hlavnej budovy
            return 'Hlavní budova'
        prod = self.get_production_per_hour()
        for v in list(prod.values())[:3]:
            if int(v) > self.get_warehouse_capacity()/8:
                return 'Sklad surovin'
        if prod['Obilí'] > self.get_granary_capacity()/8:
            return 'Sýpka'
        return self.get_lowest_resource_type()

    def rando(self,min):
        '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
        rand_secs = abs((randint((min-2)*100, (min+2)*100) / 100)*60)
        return rand_secs

