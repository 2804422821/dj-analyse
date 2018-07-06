from django.db import connection
from djanalyse import settings


class DataApp(object):
    """
    数据应用
    """
    def __init__(self, id):
        self.id = id

    def generate_store(self):
        """
        生成数据存储容器
        :return: 是否生成成功
        """
        cursor = connection.cursor()
        sql = "CREATE TABLE {db}.app_record_{id} LIKE {db}.app_record"
        sql = sql.format(db=settings.DATA_WAREHOUSE_NAME, id=self.id)
        cursor.execute(sql)
        sql = "CREATE TABLE {db}.app_record_item_{id} LIKE {db}.app_record_item"
        sql = sql.format(db=settings.DATA_WAREHOUSE_NAME, id=self.id)
        cursor.execute(sql)
        return True
