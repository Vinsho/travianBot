import time
from random import randint

def hello(msg):
    print (msg)

def rando(min):
    '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
    rand_secs = abs((randint((min-2)*100, (min+2)*100) / 100)*60)
    return rand_secs


for x in range(5):
    in_secs = rando(0.1)
    print(in_secs)
    time.sleep(in_secs)
    hello("ahoj")
