#!/usr/bin/env python3

import logging
import requests
import threading

log = logging.getLogger()

log.setLevel(logging.DEBUG)

FORMAT=logging.Formatter('[%(levelname)s] (%(threadName)-10s) %(message)s')

SH = logging.StreamHandler()
SH.setFormatter(FORMAT)
SH.setLevel(logging.INFO)
log.addHandler(SH)

FH = logging.FileHandler(filename='all.log')
FH.setFormatter(FORMAT)
log.addHandler(FH)

LOG2 = logging.getLogger('opened')
FH2 = logging.FileHandler(filename='open.log')
FH2.setFormatter(FORMAT)
FH2.setLevel(logging.DEBUG)
LOG2.addHandler(FH2)

URL = "http://portquiz.net"

THREAD_COUNT=50

MAX=66000

def worker(ports):
    print(ports)
    for port in ports:
        try:
            response = requests.get(URL + ":" + str(port), timeout=3)
            LOG2.info("Port %s open" % str(port))
        except:
            log.debug("Port %s closed" % str(port))
            continue


threads = []
for i in range(THREAD_COUNT):
    ports_ini = int(i*(MAX/THREAD_COUNT)+1)
    ports_fim = int((i+1)*(MAX/THREAD_COUNT))
    log.info('Starting thread %s' % i)
    t = threading.Thread(target=worker, args=([range(ports_ini, ports_fim)]))
    threads.append(t)
    t.start()

for th in threads:
    th.join()