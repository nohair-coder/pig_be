from rest_framework import serializers
# 类似于Django中的表单的功能，但是他可以序列化为json
from .models import Station


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'
        # depth = 1  # 外键的序列化
