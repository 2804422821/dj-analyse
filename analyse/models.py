from django.db import models
from django.contrib.auth.models import User

APP_TYPE = (
    (1, '目录'),
    (2, '报表数据源'),
)

FIELD_TYPE = (
    (1, '文本'),
    (2, '日期'),
    (3, '日期时间'),
    (4, '整数'),
    (5, '浮点数'),
    (6, '货币'),
)

YES_NO_TYPE = {
    (True, '是'),
    (False, '否'),
}


class App(models.Model):
    name = models.CharField(max_length=50, verbose_name="应用名")
    description = models.CharField(max_length=150, verbose_name="描述", blank=True)
    icon = models.ImageField(null=True, verbose_name="图标", blank=True)
    icon_ext_name = models.CharField(max_length=10, verbose_name="文件后缀", blank=True)
    icon_file_name = models.CharField(max_length=200, verbose_name="文件名", blank=True)
    icon_content = models.BinaryField(verbose_name="文件内容", null=True)
    type = models.IntegerField(choices=APP_TYPE, verbose_name="类型")
    parent_id = models.IntegerField(null=True, verbose_name="父节点")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="创建人")  # 禁止删除用户
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


class Field(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)  # 删除app的时候一并删除
    is_key = models.BooleanField(default=False, verbose_name="唯一标示")
    name = models.CharField(max_length=1000, verbose_name="字段名")
    bind_key = models.CharField(max_length=20, verbose_name="绑定标示")
    type = models.IntegerField(choices=FIELD_TYPE, verbose_name="字段类型")
    order_index = models.IntegerField(verbose_name="排序编号")
    default_show = models.BooleanField(default=True, verbose_name="默认是否显示")
    enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


class AppRecord(models.Model):
    """
    数据记录模版
    """
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now=True)
    last_update_time = models.DateTimeField(auto_now=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_record"


class AppRecordItem(models.Model):
    """
    字段值模版
    """
    record = models.ForeignKey(AppRecord, on_delete=models.CASCADE)
    field = models.IntegerField()
    field_value = models.TextField()

    class Meta:
        db_table = "app_record_item"

