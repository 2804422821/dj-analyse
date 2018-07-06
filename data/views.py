from django.shortcuts import render, HttpResponse, redirect, Http404
from django.contrib.auth.decorators import login_required
from analyse.models import App, AppRecord
from  djanalyse import settings


@login_required
def data_list(request):
    """
    app列表
    """
    apps = App.objects.filter(creator=request.user)
    return render(request, 'list.html', {"apps": apps})


def data_record(request, app_id):
    """
    数据列表
    """
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        raise Http404("你所访问的页面不存在")

    sql = "select * from {db}.app_record_{app_id} where creator_id = {creator}"
    sql = sql.format(db=settings.DATA_WAREHOUSE_NAME, app_id=app_id, creator=request.user.id)
    records = AppRecord.objects.raw(sql)

    return render(request, 'record.html', {"app": app, "records": records})

