import time
import datetime
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    filename='log.txt',
                    filemode='w')


def next_build(rand_secs):
    buildin_in = time.time() + rand_secs
    logging.warning("Next build at: " + datetime.datetime.fromtimestamp(buildin_in).strftime('%Y-%m-%d %H:%M:%S') + '\n')


def building(res, id, lvl):
    logging.warning("Building " + res + " with id=" + str(id + 1) + ' to lvl '+str(lvl+1) + '\n')


def write_excep(s,msg):
    up_in = time.time() + s
    logging.warning(msg+ ", puttin myself to sleep, will be up at " + datetime.datetime.fromtimestamp(up_in).strftime('%Y-%m-%d %H:%M:%S') + '\n')