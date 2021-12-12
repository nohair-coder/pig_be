from django.db import models

# Create your models here.


class Station(models.Model):
    choice = (
        ('ON', '运行中'),  # 绿色
        ('OFF', '已关机'),  # 黑色
        ('ERROR', '有故障')  # 红色
    )
    build_unit_station = models.CharField(max_length=8, unique=True, verbose_name='饲喂站号')
    status = models.CharField(choices=choice, default='OFF', max_length=8, verbose_name="状态")
    temperature = models.FloatField(default=25, verbose_name='温度')  # 温度
    humidity = models.FloatField(default=0.4, verbose_name='温度')  # 湿度
    status_num = models.CharField(max_length=20, default=0, verbose_name='状态码')

    class Meta:
        db_table = 'tb_station'  # 指明数据库表名
        verbose_name = '饲喂站信息'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.build_unit_station
