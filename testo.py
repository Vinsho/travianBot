import time
from random import randint
import re

def hello(msg):
    print (msg)

def rando(min):
    '''vracia random cas v intervale (min-2,min+2) v sekundach a vypise kedy sa to stane'''
    rand_secs = abs((randint((min-2)*100, (min+2)*100) / 100)*60)
    return rand_secs
string="\u200e\u202d(\u202d-105\u202c|\u202d4\u202c)\u202c\u200e"
print([re.search(r'\b\d+\b', string).group(0)])

