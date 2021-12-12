# coding: utf8
import requests
import json
from ..WLAN_4G import Handle4G
from ..station.models import Station

import random

baseURL = 'http://www.hzaupig.work:8055/'


def pigPost(json_object):
    """下位机母猪入栏"""
    try:
        pigId = 'error' + ''.join(random.choice("0123456789") for i in range(11))
        maleId = ''.join(random.choice("0123456789") for i in range(16))
        data_object = {}
        data_object['pigId'] = pigId
        data_object['maleId'] = maleId
        data_object['stationId'] = json_object['stationid']
        data_object['earId'] = json_object['earid']
        data_object['breedTime'] = json_object['mating_date']
        data_object['gestationalAge'] = json_object['parity']
        data_object['backFat'] = json_object['backfat']
        r = requests.post(baseURL + 'pigbase/', json=data_object)
        ack = json.loads(r.text)
        if ack['code'] != 'success':
            print('pigPost', ack)
            print('pigPost err', json_object)
            return False
        else:
            return True
    except:
        print('pigPost failed !')
        return False


def dataPost(json_object):
    """数据上传"""
    try:
        print('json_object', json_object)
        r = requests.post(baseURL + 'feedingdata/', json=json_object)
        # r = requests.post("http://httpbin.org/post", data=payload)
        ack = json.loads(r.text)
        if ack['code'] != 'success':
            print('dataPost', ack)
            print('dataPost err', json_object)
            return False
        else:
            return True
    except:
        print('dataPost failed !')
        return False


def devicePost(json_object):
    """设备新增"""
    try:
        r = requests.post(baseURL + 'station/', json=json_object)
        ack = json.loads(r.text)
        print('devicePost ackackackackack', ack)
        # if ack['code'] != 'success':
        #     print('devicePost', ack['code'])
    except:
        print('devicePost connect failed !')
        return False


def devicePut(json_object):
    """设备状态修改"""
    try:
        one = Station.objects.get(build_unit_station=json_object['build_unit_station'])
        one.status = json_object['status']
        one.save()
        return True
    except:
        print('devicePut connect failed !')
        return False
