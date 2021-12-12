from apps.station.models import Station
from apps.pig_base.models import PigBase
from apps.feeding_set.models import FeedingSet
from .pig_id_kind import pig_id_kind
import datetime
import random
import string


def algo_backfat(backfat):
    """
    依据背膘厚计算出的饲喂量，算法饲喂量
    :param backfat:
    :return:
    """
    algo_intake = backfat * 2
    return algo_intake


def write_pigbase(req):
    """
    把数据写入母猪基础表
    :param req:
    :return:
    """
    P = PigBase()
    P.stationId = Station.objects.get(build_unit_station=req['stationId'])
    P.pigId = req['pigId']
    P.earId = req['earId']
    P.breedTime = req['breedTime']
    P.maleId = req['maleId']
    P.gestationalAge = req['gestationalAge']
    P.save()
    print('write_pigbase')


# def write_backfat(req):
#     """
#     把数据写入背膘厚表
#     :param req:
#     :return:
#     """
#     B = Backfat()
#     B.pigid = PigBase.objects.get(pigid=req['PigId'])
#     if req['BackFat'] != '':
#         B.backfat = req['BackFat']
#     else:
#         B.backfat = None
#     B.save()
#     # print('write_backfat')


def write_foodquantity(req):
    """
    把数据写入饲喂量表
    :param req:
    :return:
    """
    F = FeedingSet()
    F.pigId = PigBase.objects.get(pigId=req['pigId'])
    if req['backFat'] != '':
        F.backFat = req['backFat']
        F.algoQuantity = algo_backfat(float(req['backFat']))
    else:
        F.backFat = None
    F.save()
    # print('write_foodquantity')


def get_pig_kind(pigid):
    """
    根据母猪号后两位获取品种
    :param pigid:
    :return:
    """
    kind_id = pigid[-2:]
    return pig_id_kind[kind_id]


def delete_pigbase(req):
    """
    离栏，在pigbase表中添加离栏时间，而不是删除猪只
    :param req: 母猪号
    :return:
    """
    now_time = datetime.datetime.now().strftime('%F')
    sub_pig = PigBase.objects.get(pigid=req)
    sub_pig.decpigtime = now_time
    sub_pig.save()


def generate_pigid_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 15))
    return salt
