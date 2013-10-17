import socket
import time
import re
#import logging

#logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s\t Thread-%(thread)d - %(message)s", filename='/tmp/gmond.log', filemode='w')
#logging.debug('starting up')

def metric_handler(name):

    match = re.search(r"redis-llen_(\d+)_(\w+)",name)
    if not match:
         return 1
    database = match.group(1)
    list = match.group(2)

    if (database not in metric_handler.databases) or (list not in metric_handler.lists):
        return 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((metric_handler.host, metric_handler.port))
    s.send("SELECT %s\r\n" % database)
    info = s.recv(4096)
    s.send("LLEN %s\r\n" % list)
    info = s.recv(4096)

    metric_handler.info = {}
    if ":" != info[0]:
        return 0

    try:
          n, v = info.split(":")
          metric_handler.info[name] = int(v) 
    except Exception, e:
        logging.debug("caught exception %s" % e)
        pass

    s.close()

    #logging.debug("returning metric_handl: %s %s %s" % (metric_handler.info.get(name, 0), metric_handler.info, metric_handler))
    return metric_handler.info.get(name, 0)

def metric_init(params={}):
    metric_handler.host = params.get("host", "127.0.0.1")
    metric_handler.port = int(params.get("port", 6379))

    databases = params.get("databases", "0");
    metric_handler.databases = []
    if databases.__len__() > 0:
        metric_handler.databases = map(str.strip, databases.split(','))

    lists = params.get("lists", "");
    metric_handler.lists = []
    if lists.__len__() > 0:
        metric_handler.lists = map(str.strip, lists.split(','))

    metrics = {
        "redis-llen": {"units": "items"},
    }
    metric_handler.descriptors = {}

    for database in metric_handler.databases:
        for list in metric_handler.lists:
            for base_name, updates in metrics.iteritems():
                name = "%s_%s_%s" % (base_name, database, list)
                descriptor = {
                    "name": name,
                    "call_back": metric_handler,
                    "time_max": 90,
                    "value_type": "int",
                    "units": "",
                    "slope": "both",
                    "format": "%d",
                    "description": "http://redis.io/commands/llen",
                    "groups": "redis_list_size_%s" % database,
                }
                descriptor.update(updates)
                metric_handler.descriptors[name] = descriptor
    return metric_handler.descriptors.values()



def metric_cleanup():
    pass

#This code is for debugging 
if __name__ == '__main__':
    params = {'databases': '0,1, 2', 'lists': 'listA, listB,listC'}
    metric_init(params)
    for d in metric_handler.descriptors.values():
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'], v)
