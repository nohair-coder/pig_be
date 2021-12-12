# import requests
#
# baseURL = 'http://localhost:8000/'
#
# try:
#
#     json_object = {'build_unit_station': '01-01-0001', 'status_num': '00000', 'status': 'on'}
#
#     r = requests.patch(baseURL + 'station/' + '1' + '/', data=json_object)
#     # ack = json.loads(r.text)
#     print('devicePut ackackackackack', r.status_code)
# except:
#     print('devicePut connect failed !')
import time

a = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime('20201213101914', "%Y%m%d%H%M%S"))
print(a)
# {
#     "func": "addpig",
#     "stationid": "01020003",
#     "earid": "12345678",
#     "mating_date": "20190304",
#     "parity": 3,
#     "backfat": 13.1
# }
# {
#     "func": "intake",
#     "stationid": "01020004",
#     "earid": "00000005",
#     "food_intake": 100,
#     "start_time": "20201213101914",
#     "end_time": "20201213101914"
# }
