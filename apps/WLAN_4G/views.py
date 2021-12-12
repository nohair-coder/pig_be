from .sync_stationinfo import sync_stationinfo
from .Handle4G import Analysis_sysInit
from ..station.models import Station


def get_station_id_list():
    stations = Station.objects.values('build_unit_station')
    s_list = []
    for item in stations:
        s_list.append(item['build_unit_station'])

    return s_list


Analysis_sysInit(get_station_id_list)
sync_stationinfo()
