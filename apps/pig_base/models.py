from django.db import models
from apps.station.models import Station
# Create your models here.


class PigBase(models.Model):
    stationId = models.ForeignKey(Station,
                                  to_field='build_unit_station',
                                  on_delete=models.CASCADE,
                                  verbose_name='饲喂站号')
    pigId = models.CharField(max_length=16, unique=True, verbose_name='身份码')
    earId = models.CharField(max_length=8, verbose_name='耳标号')
    pigKind = models.CharField(max_length=20, verbose_name='品种', null=True)
    maleId = models.CharField(max_length=16, null=True, verbose_name='与配公猪号')
    gestationalAge = models.FloatField(default=0, verbose_name='胎龄')
    # vaccine = models.CharField(max_length=64, verbose_name='疫苗情况')
    addpigtime = models.DateField(auto_now_add=True, verbose_name='入栏日期')
    breedTime = models.CharField(max_length=16, verbose_name='配种日期')
    decpigtime = models.DateField(max_length=10, null=True, verbose_name='出栏日期')

    class Meta:
        db_table = 'tb_pig_base'  # 指明数据库表名
        verbose_name = '动物基础表'  # 在admin站点中显示的名称
        unique_together = ('stationId', 'earId',)
        # verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.stationId
