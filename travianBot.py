import requests
import Build


starting_url = 'https://ts1.travian.cz/dorf1.php'


class Travian:
    def __init__(self, username, password):
        self.session = self.login(username, password)

    def login(self, username, password):
        '''prihlasi sa na ucet a vrati session'''
        data = {'login': '1526489272', 'name': username, 'password': password, 's1': 'Přihlásiť+se',
                'w': '1920:1080'}

        with requests.session() as session:
            session.headers.update({'x-test': 'true'})
            session.post(starting_url, data)
            return session

if __name__ == '__main__':
    travian = Travian("Scasike", "firebrand")
    Build.repetitive_build(session)
