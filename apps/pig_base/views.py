from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import PigBase
from .logic import write_pigbase, write_foodquantity, delete_pigbase, generate_pigid_str
import datetime


class PigBaseView(APIView):
    def get(self, request):
        pageNo = int(request.query_params['pageNo'])
        pageSize = int(request.query_params['pageSize'])
        all_pig = PigBase.objects.all()
        data = []
        try:
            pigs = PigBase.objects.filter(id__range=((pageNo - 1) * pageSize + 1, pageNo * pageSize))
            today = datetime.date.today()
            d1 = datetime.datetime(today.year, today.month, today.day)
            for item in pigs:
                d2 = datetime.datetime(int(item.breedTime[0:4]), int(item.breedTime[4:6]), int(item.breedTime[6:8]))
                data.append({
                    'id': item.id,
                    'stationId': item.stationId_id,
                    'pigId': item.pigId,
                    'earId': item.earId,
                    'maleId': item.maleId,
                    'breedTime': item.breedTime,
                    'backFat': item.feedingset_set.get(pigId=item.pigId).backFat,
                    'gestationalAge': item.gestationalAge,
                    'days': (d1 - d2).days + 1
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
        try:
            req = request.data
            # print(req)
            exist_pigid = PigBase.objects.filter(
                Q(pigId=req['pigId']) & Q(decpigtime=None))
            exist_earid = PigBase.objects.filter(
                Q(stationId=req['stationId']) & Q(earId=req['earId']) & Q(decpigtime=None))
            if exist_pigid:
                return Response({'code': 0, 'message': '该母猪号已存在，请检查输入'})
            elif exist_earid:
                return Response({'code': 0, 'message': '该栏中耳标号已存在，请选择其它耳标'})
            else:
                write_pigbase(req)
                write_foodquantity(req)
                return Response({'code': 1, 'message': '入栏成功'})
        except Exception as e:
            print(e)
            return Response({'code': 0, 'message': '入栏失败'})

    def delete(self, request):
        return Response('PigBaseView delete OK')
        
    def patch(self, request):
        # 更换耳标
        return Response('PigBaseView patch OK')

    def put(self, request):
        # 转栏
        req = request.data
        print(req)
        return Response('PigBaseView put OK')
