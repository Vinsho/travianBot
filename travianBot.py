import requests
import Build


starting_url = 'https://ts3.travian.cz'


class Travian:
    def __init__(self, username, password, start_url):
        self.session = self.login(username, password)
        self.url = start_url

    def login(self, username, password):
        '''prihlasi sa na ucet a vrati session'''
        data = {'login': '1526489272', 'name': username, 'password': password, 's1': 'Přihlásiť+se',
                'w': '1920:1080'}

        with requests.session() as session:
            session.headers.update({'x-test': 'true'})
            session.post(starting_url+"/dorf1.php", data)
            return session

if __name__ == '__main__':
    travian = Travian("Scasike", "firebrand", starting_url)
    Build.repetitive_build(session)
