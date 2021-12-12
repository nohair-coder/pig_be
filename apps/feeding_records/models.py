from django.db import models
from apps.pig_base.models import PigBase


# Create your models here.
class FeedingRecords(models.Model):
    pigid = models.ForeignKey(PigBase, to_field='pigId', verbose_name='身份码', on_delete=models.CASCADE)
    food_intake = models.FloatField(verbose_name='采食量')
    start_time = models.DateTimeField(verbose_name='开始进食时间')  # 开始进食时间
    end_time = models.DateTimeField(verbose_name='结束进食时间')  # 结束进食时间
    sys_time = models.DateTimeField(auto_now_add=True, verbose_name='服务器本地时间')  # 服务器本地时间

    class Meta:
        db_table = 'tb_feeding_records'  # 指明数据库表名
        verbose_name = '动物采食信息表'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.pigid
