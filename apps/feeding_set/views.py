import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FeedingSet
from apps.pig_base.models import PigBase


# Create your views here.


class FeedingSetView(APIView):
    def get(self, request):
        pageNo = int(request.query_params['pageNo'])
        pageSize = int(request.query_params['pageSize'])
        all_pig = PigBase.objects.all()
        data = []
        try:
            pigs = PigBase.objects.filter(id__range=((pageNo - 1) * pageSize + 1, pageNo * pageSize))
            for item in pigs:
                temp = item.feedingset_set.filter(pigId=item.pigId).order_by('-setTime').first()
                data.append({
                    'id': item.id,
                    'pigId': item.pigId,
                    'earId': item.earId,
                    'stationId': item.stationId_id,
                    'backFat': temp.backFat,
                    'indexQuantity': temp.indexQuantity,
                    'algoQuantity': temp.algoQuantity,
                    'setQuantity': temp.algoQuantity,
                    'setTime': temp.setTime
                })
        except:
            data = []
        response = {
            'data': data,
            'pageNo': pageNo,
            'pageSize': pageSize,
            'totalCount': len(all_pig),
            'totalPage': 1
        }
        return Response(response)

    def post(self, request):
        return Response('FeedingSetView post OK')

    def delete(self, request):
        return Response('FeedingSetView delete OK')

    def put(self, request):
        return Response('FeedingSetView put OK')
