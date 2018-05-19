import requests
from Build import Build
from Hero import *
from Army import *


starting_url = 'https://ts3.travian.cz'


class Travian:
    def __init__(self, username, password, start_url, debug=False):
        self.session = self.login(username, password)
        self.url = start_url

        self.build = Build(self.session, self.url, debug)
        self.hero = Hero(self.session, self.url, debug)
        self.army = Army(self.session, self.url, debug)

    def login(self, username, password):
        '''prihlasi sa na ucet a vrati session'''
        data = {'login': '1526489272', 'name': username, 'password': password, 's1': 'Přihlásiť+se',
                'w': '1920:1080'}

        with requests.session() as session:
            session.headers.update({'x-test': 'true'})
            session.post(starting_url+"/dorf1.php", data)
            return session


if __name__ == '__main__':
    travian = Travian("Scasike", "firebrand", starting_url, True)
    #travian.build.build_lowest()
    #travian.hero.go_on_first_to_expire_adventure()
    troops = travian.army.get_troops()
    print(travian.army.translator(troops))
