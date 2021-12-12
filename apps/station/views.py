from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Station
from apps.WLAN_4G.HttpStation import openOrClose


# Create your views here.


class StationView(APIView):
    def get(self, request):
        pageNo = int(request.query_params['pageNo'])
        pageSize = int(request.query_params['pageSize'])
        all_station = Station.objects.all()
        data = []
        try:
            stations = Station.objects.filter(id__range=((pageNo - 1) * pageSize + 1, pageNo * pageSize))
            for item in stations:
                data.append({
                    'id': item.id,
                    'build_unit_station': item.build_unit_station,
                    'temperature': item.temperature,
                    'humidity': item.humidity,
                    'status': item.status
                })
        except:
            data = []
        response = {
            'data': data,
            'pageNo': pageNo,
            'pageSize': pageSize,
            'totalCount': len(all_station),
            'totalPage': 2
        }
        return Response(response)

    def post(self, request):
        try:
            req = request.data
            req_build_unit_station = req['build_unit_station']
            exist_station = Station.objects.filter(build_unit_station=req_build_unit_station).first()
            if exist_station is None:
                s = Station()
                s.build_unit_station = req_build_unit_station
                s.save()
                return Response({'code': 1, 'message': 'Station addition OK'})
            else:
                return Response({'code': 0, 'message': '饲喂站已存在,请重新输入'})
        except:
            return Response({'code': 0, 'message': '添加失败，请重试'})


class HandleStationView(APIView):
    def get(self, request):
        all_station = Station.objects.all()
        data = [item.build_unit_station for item in all_station]
        return Response(data)

    def post(self, request):
        req = request.data
        print(req)
        if openOrClose(req):
            return Response({'code': 1, 'message': '修改饲喂站状态成功'})
        else:
            return Response({'code': 0, 'message': '修改饲喂站状态失败'})

    def delete(self, request):
        return Response('HandleStationView delete OK')

    def put(self, request):
        return Response('HandleStationView put OK')
