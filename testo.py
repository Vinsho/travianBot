import time
import datetime
import schedule
from random import randint

def hello(msg):
    print (msg)
timo = (randint(1000, 1300) / 100)*60
print(timo)
time = time.time()+timo
print(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
