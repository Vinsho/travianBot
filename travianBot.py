import requests
from Build import Build
from Hero import *
from Army import *
import time
import Messages

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


def automat():
    while True:
        travian = Travian("Scasike", "firebrand", starting_url, True)
        secs = travian.build.rando(20)
        adventures = travian.hero.get_adventures()
        if adventures != {} and travian.hero.get_hero_status() == "v domovské vesnici":
            travian.hero.go_on_first_to_expire_adventure()
        travian.build.build(travian.build.what_to_build())
        Messages.build_at(secs)
        time.sleep(secs)

if __name__ == '__main__':
    automat()
    # travian = Travian("Scasike", "firebrand", starting_url, True)
    #print(travian.build.get_production_per_hour())
    # travian.build.build(travian.build.what_to_build())
    # troops = travian.army.translator(travian.army.get_troops())
    # travian.army.send_raid(troops,-34,74)


