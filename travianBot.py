import requests
import Build


starting_url = 'https://ts1.travian.cz/dorf1.php'


def login():
    data = {'login': '1526489272', 'name': 'Scasike', 'password': 'firebrand', 's1': 'Přihlásiť+se',
            'w': '1920:1080'}

    with requests.session() as session:
        session.headers.update({'x-test': 'true'})
        session.post(starting_url, data)
        return session

session=login()
Build.build(session)
