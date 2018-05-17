import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import schedule
from random import randint


def get_connected_devices():
    in_min = 11
    starting_url = 'https://ts1.travian.cz/dorf1.php'
    data = {'login': '1526489272', 'name': 'Scasike', 'password': 'firebrand', 's1': 'Přihlásiť+se',
            'w': '1920:1080'}

    with requests.session() as session:
        session.headers.update({'x-test': 'true'})
        session.post(starting_url, data)
        r = session.get(starting_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        schedule.every(rando(in_min)).seconds.do(build,session=session, soup=soup) #zavola stavanie kazdych +-in_min minut
    while True:
        schedule.run_pending()
        time.sleep(1)


def resources(soup):
    res = soup.find_all('span',{'class': 'value'})
    resources = {"drevo": (res[1].contents[0]), "hlina": res[2].contents[0], "zelezo": res[3].contents[0],
                 "obilie": res[5].contents[0]}
    for k, v in resources.items():
        resources[k] = re.search(r'\b\d+\b', v).group(0)
    return resources


def rando(min):
    '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
    rand_secs = (randint((min-2)*100, (min+2)*100) / 100)*60
    buildin_in = time.time() + rand_secs
    print("next build at: " + datetime.datetime.fromtimestamp(buildin_in).strftime('%Y-%m-%d %H:%M:%S'))
    return rand_secs


def build(session, soup):
    enum={'drevo': [0,2,13,16], 'hlina': [4,5,15,17], 'zelezo': [3,6,9,10], 'obilie': [1,7,8,11,12,14]}
    res=resources(soup)
    min_res = str(min(res, key=lambda x: res[x]))
    print(res)
    print(min_res)
    lvls = []
    for each in soup.find_all('area'):
        lvls += each.get('alt')
    lvls = [x for x in lvls if x.isdigit()]
    chosen_one = int(enum[min_res][0])
    for x in enum[min_res]:
        if int(lvls[x]) < int(lvls[chosen_one]):
            chosen_one = int(x)
    #i = int(next(x for x in range(len(lvls)) if (lvls[x] == min(lvls)))) + 1 # pole s najnizsim/min levelom
    print("building "+ min_res + str(chosen_one+1))
    r = session.get('https://ts1.travian.cz/build.php?id='+str(chosen_one+1))
    soup = BeautifulSoup(r.content, 'html.parser')
    temp = soup.find('button', {'class': 'green build'})  # ziska link postavania budovy
    session.post('https://ts1.travian.cz/' + temp['onclick'].split("'")[1])


get_connected_devices()