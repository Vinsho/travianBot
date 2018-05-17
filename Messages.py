import time
import datetime

def build_at(rand_secs):
    buildin_in = time.time() + rand_secs
    print("next build at: " + datetime.datetime.fromtimestamp(buildin_in).strftime('%Y-%m-%d %H:%M:%S'))