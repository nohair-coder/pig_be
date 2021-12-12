import json
from .Handle4G import device_status, Send_4G_Queue


def openOrClose(json_object):
    order = ''
    try:
        node = json_object['build_unit_station']
        set_status = json_object['status']
        if set_status == 'ON':
            order = '$' + node + '102' + '#'
        elif set_status == 'OFF':
            order = '$' + node + '201' + '#'
        print('order', order)
        Send_4G_Queue.put([order, device_status[node]['addr']])
        return True
    except:
        return False


def setFood(json_object):
    print(json_object)
