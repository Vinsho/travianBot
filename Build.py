from bs4 import BeautifulSoup
import re
import schedule
import time
import datetime
from random import randint

starting_url = 'https://ts1.travian.cz/dorf1.php'

def resources(soup):
    res = soup.find_all('span',{'class': 'value'})
    resources = {"drevo": (res[1].contents[0]), "hlina": res[2].contents[0], "zelezo": res[3].contents[0],
                 "obilie": res[5].contents[0]}
    for k, v in resources.items():
        resources[k] = re.search(r'\b\d+\b', v).group(0)
    return resources


def build(session):
    r = session.get(starting_url)
    soup = BeautifulSoup(r.content, 'html.parser')
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
    print("building "+ min_res + str(chosen_one+1))
    r = session.get('https://ts1.travian.cz/build.php?id='+str(chosen_one+1))
    soup = BeautifulSoup(r.content, 'html.parser')
    temp = soup.find('button', {'class': 'green build'})  # ziska link postavania budovy
    session.post('https://ts1.travian.cz/' + temp['onclick'].split("'")[1])


def repetitive_build(session):
    in_min = 11
    r = session.get(starting_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    schedule.every(rando(in_min)).seconds.do(build, session=session)  # zavola stavanie kazdych +-in_min minut
    while True:
        schedule.run_pending()
        time.sleep(1)


def rando(min):
    '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
    rand_secs = (randint((min-2)*100, (min+2)*100) / 100)*60
    buildin_in = time.time() + rand_secs
    print("next build at: " + datetime.datetime.fromtimestamp(buildin_in).strftime('%Y-%m-%d %H:%M:%S'))
    return rand_secs