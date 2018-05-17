import travianBot
from bs4 import BeautifulSoup

def get_troops(session,url):

    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    keys = soup.find_all('td',{'class': 'un'})
    keys = [k.text for k in keys]
    values = soup.find_all('td',{'class': 'num'})
    values = [v.text for v in values[4:]]
    troops=dict(zip(keys,values))
    print(troops)

if __name__ == "__main__":
    travian = travianBot.Travian("Scasike", "firebrand",'https://ts3.travian.cz/dorf1.php')
    get_troops(travian.session,travian.url)