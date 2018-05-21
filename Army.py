import travianBot
from bs4 import BeautifulSoup

class Army:
    def __init__(self,session,url,debug):
        self.session = session
        self.debug = debug
        self.url = url + '/dorf1.php'
        self.troop_send_url = url + '/build.php?tt=2&id=39'
        self.confirm_troop_send_url = url + '/build.php?id=39&tt=2'

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

    def send_raid(self, troops, x, y):
        soup = self.get_soup(self.troop_send_url)
        hidden_tags = soup.findAll('input',{'type': 'hidden'})
        data = {tag['name']: tag['value'] for tag in hidden_tags}
        for k, v in troops.items():
            data.update({k: v})
        data.update({'x': x, 'y': y, 'c': '4', 's1': 'ok'})
        confirmation = self.session.post(self.troop_send_url, data).content
        soup = BeautifulSoup(confirmation, 'html.parser')
        hidden_tags = soup.findAll('input', {'type': 'hidden'})
        data = {tag['name']: tag['value'] for tag in hidden_tags}
        data['s1'] = 'ok'
        self.session.post(self.confirm_troop_send_url, data)


    def translator(self,troops):
        '''premeni keys(f.e.Pálkařů) na t1,t2..'''
        table = {'Pálkařů': 't1','Hrdina': 't11'}
        translated = {table[k]: v for k, v in troops.items()}
        return translated

if __name__ == "__main__":
    sewa