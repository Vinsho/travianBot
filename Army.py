import travianBot
from bs4 import BeautifulSoup

class Army:
    def __init__(self,session,url,debug):
        self.session = session
        self.debug = debug
        self.url = url + '/dorf1.php'
        self.troop_send_url = url + '/build.php?tt=2&id=39'

    def get_soup(self,url):
        return BeautifulSoup(self.session.get(url).content, 'html.parser')

    def get_troops(self):
        soup = self.get_soup(self.url)
        keys = soup.find_all('td',{'class': 'un'})
        keys = [k.text for k in keys]
        values = soup.find_all('td',{'class': 'num'})
        values = [v.text for v in values[4:]]
        troops = dict(zip(keys,values))
        return troops

    # def sent_troops(self,troops,x,y):
    #     soup = travian.get_soup(self.troop_send_url)
    #     for troops.items

    def translator(self,troops):
        '''premeni keys(f.e.Pálkařů) na t1,t2..'''
        table = {'Pálkařů': 't1'}
        translated = {table[k]: v for k, v in troops.items()}
        return translated

if __name__ == "__main__":
    travian = travianBot.Travian("Scasike", "firebrand",'https://ts3.travian.cz/dorf1.php')
