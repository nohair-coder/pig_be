from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import FeedingRecords
from apps.pig_base.models import PigBase
from django.db.models import Q
import time


# Create your views here.


class FeedingDataView(APIView):
    def get(self, request):
        pageNo = int(request.query_params['pageNo'])
        pageSize = int(request.query_params['pageSize'])
        all_records = FeedingRecords.objects.all()
        data = []
        try:
            r = FeedingRecords.objects.filter(id__range=((pageNo - 1) * pageSize + 1, pageNo * pageSize))
            for item in r:
                data.append({
                    'id': item.id,
                    'stationId': PigBase.objects.get(pigId=item.pigid_id).stationId_id,
                    'pigId': item.pigid_id,
                    'earId': PigBase.objects.get(pigId=item.pigid_id).earId,
                    'mount': item.food_intake,
                    'startTime': item.start_time,
                    'endTime': item.end_time,
                    'backFat': PigBase.objects.get(pigId=item.pigid_id).feedingset_set.get(pigId=item.pigid_id).backFat
                })
        except Exception as e:
            print(e)
            data = []
        response = {
            'data': data,
            'pageNo': pageNo,
            'pageSize': pageSize,
            'totalCount': len(all_records),
            'totalPage': 1
        }
        return Response(response)


    def post(self, request):
        try:
            req_earid = request.data['earid']
            req_stationid = request.data['stationid']
            exist = PigBase.objects.get(earId=req_earid, stationId=req_stationid).pigId
            I = FeedingRecords()
            I.pigid = PigBase.objects.get(pigId=exist)
            I.food_intake = request.data['food_intake']
            I.start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.strptime(request.data['start_time'], "%Y%m%d%H%M%S"))
            I.end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.strptime(request.data['end_time'], "%Y%m%d%H%M%S"))
            I.save()
            return Response({'code': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'code': 'error'}, status=status.HTTP_200_OK)


# {
#     'func': 'intake',
#     'stationid': '01020003',
#     "earid": "00000004",
#     "food_intake": 100,
#     "start_time": "20200927050607",
#     "end_time": "20200927050814"
# }


