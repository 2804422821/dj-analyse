from django.shortcuts import render, HttpResponse, redirect, Http404
from .forms import EditAppForm, FieldForm
from .models import App, Field
from django.db.models import F
from django.contrib.auth.decorators import login_required
import uuid
import os
from django.views.decorators.csrf import csrf_exempt
from analyse_core.app import DataApp
from django.db import IntegrityError, transaction


@login_required
def app_list(request):
    """
    app列表
    """
    apps = App.objects.filter(creator=request.user)
    return render(request, 'app/list.html', {"apps": apps})


@login_required
def app_add(request):
    """
    添加app
    """
    if request.method == "GET":
        form = EditAppForm()
        return render(request, "app/add.html", {"form": form})
    else:
        app_form = EditAppForm(request.POST)
        if app_form.is_valid():
            new_app = app_form.save(commit=False)
            new_app.creator = request.user

            # 保存图片
            icon = request.FILES.get('icon', None)
            if icon is not None:
                file = 'static/uploads/app/thumbnail/'
                if not os.path.exists(file):
                    os.makedirs(file)

                new_app.icon_ext_name = os.path.splitext(icon.name)[1]
                new_app.icon_file_name = (str(uuid.uuid1()) + new_app.icon_ext_name)
                new_app.icon = (file + new_app.icon_file_name)

                f = open(os.path.join(str(new_app.icon)), 'wb+')
                for line in icon.chunks():
                    f.write(line)
                f.close()

                with open(str(new_app.icon), 'rb') as f:
                    new_app.icon_content = f.read()

            new_app.save()

            # 生成数据表
            data_app = DataApp(id=new_app.id)
            data_app.generate_store()

            if request.POST["submit"] == 'save':
                return redirect("/analyse/app/list")
            else:
                return redirect("/analyse/field/list/" + str(new_app.id))
        else:
            return render(request, "lapp/add.html", {'errorMsg': '添加数据应用失败', "form": app_form})


@csrf_exempt
@login_required
def app_name_not_exists(request):
    """
    判断app名称是否不存在
    """
    name = request.POST["name"]
    try:
        App.objects.get(name=name, creator=request.user)
    except App.DoesNotExist:
        return HttpResponse("true")
    return HttpResponse("false")


@login_required
def app_edit(request, id):
    """
    编辑app
    :param request:
    :param id: app编号
    :return:
    """
    try:
        app = App.objects.get(id=id)
    except App.DoesNotExist or app.creator != request.user:
        raise Http404("你所访问的页面不存在")

    if request.method == "GET":
        form = EditAppForm(initial={"name": app.name, "description": app.description, "type": app.type})
        return render(request, 'app/edit.html', {"app": app, "form": form})
    else:
        app_form = EditAppForm(request.POST)
        if app_form.is_valid():
            app.type = app_form.cleaned_data["type"]
            app.name = app_form.cleaned_data["name"]
            app.description = app_form.cleaned_data["description"]

            # 保存图片
            icon = request.FILES.get('icon', None)
            if icon is not None:
                file = 'static/uploads/app/thumbnail/'

                # 删除以前的图片
                if app.icon != '' and os.path.exists(app.icon):
                    os.remove(app.icon)

                if not os.path.exists(file):
                    os.makedirs(file)

                app.icon_ext_name = os.path.splitext(icon.name)[1]
                app.icon_file_name = (str(uuid.uuid1()) + app.icon_ext_name)
                app.icon = (file + app.icon_file_name)

                f = open(os.path.join(str(app.icon)), 'wb+')
                for line in icon.chunks():
                    f.write(line)
                f.close()

                with open(str(app.icon), 'rb') as f:
                    app.icon_content = f.read()

            app.save()
            return redirect("/analyse/app/list")
        else:
            return render(request, "app/edit.html", {'errorMsg': '更新数据应用失败', "app": app, "form": app_form})


@login_required
def field_list(request, app_id):
    """
    字段列表
    """
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        raise Http404("你所访问的页面不存在")

    fields = Field.objects.filter(app=app_id, is_delete=False).order_by("order_index")
    return render(request, 'field/list.html', {"fields": fields, "app": app})


@login_required
def field_add(request, app_id):
    """
    添加字段
    :param request:
    :param app_id: app编号
    :return:
    """
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        raise Http404("你所访问的页面不存在")

    if request.method == "GET":
        form = FieldForm()
        return render(request, 'field/add.html', {"app": app, "form": form})
    else:
        field_form = FieldForm(request.POST)
        if field_form.is_valid():
            new_field = field_form.save(commit=False)
            new_field.app = app
            new_field.order_index = Field.objects.filter(app=app).count() + 1
            new_field.save()
            if new_field.bind_key == '':
                new_field.bind_key = 'fkey' + str(new_field.id)
            new_field.save()
            return redirect("/analyse/field/list/" + str(app.id))
        else:
            return render(request, "field/add.html", {'errorMsg': '添加字段失败', "app": app, "form": field_form})


@csrf_exempt
@login_required
def field_name_not_exists(request, app_id):
    """
    判断field名称是否不存在
    """
    name = request.POST["name"]
    try:
        field = Field.objects.get(name=name, app=app_id, is_delete=False)
        if request.POST.get('exclude', None) and str(field.id) == request.POST["exclude"]:
            return HttpResponse("true")
    except Field.DoesNotExist:
        return HttpResponse("true")
    return HttpResponse("false")


@csrf_exempt
@login_required
def field_bind_name_not_exists(request, app_id):
    """
    判断field绑定名称是否不存在
    """
    name = request.POST["name"]
    try:
        field = Field.objects.get(bind_key=name, app=app_id, is_delete=False)
        if request.POST.get('exclude', None) and str(field.id) == request.POST["exclude"]:
            return HttpResponse("true")
    except Field.DoesNotExist:
        return HttpResponse("true")
    return HttpResponse("false")


@login_required
def field_edit(request, id):
    """
    编辑字段
    :param request:
    :param id: 字段编号
    :return:
    """
    try:
        field = Field.objects.get(id=id, is_delete=False)
        app = App.objects.get(id=field.app_id)
        if app.creator != request.user:
            raise Http404("你所访问的页面不存在")
    except Field.DoesNotExist or App.DoesNotExist:
        raise Http404("你所访问的页面不存在")

    if request.method == "GET":
        form = FieldForm(initial={"name": field.name, "is_key": field.is_key, "bind_key": field.bind_key, "default_show": field.default_show, "type": field.type})
        return render(request, 'field/edit.html', {"app": app, "form": form, "field": field})
    else:
        if request.POST["submit"] == 'save':
            field_form = FieldForm(request.POST)
            if field_form.is_valid():
                field.name = field_form.cleaned_data["name"]
                field.bind_key = field_form.cleaned_data["bind_key"]
                field.is_key = field_form.cleaned_data["is_key"]
                field.default_show = field_form.cleaned_data["default_show"]
                field.type = field_form.cleaned_data["type"]
            else:
                return render(request, "field/edit.html", {'errorMsg': '修改字段失败', "app": app, "form": field_form,
                                                           "field": field})
        elif request.POST["submit"] == 'enable':
            field.enable = not field.enable
        else:
            field.enable = False
            field.is_delete = True
        field.save()
        return redirect("/analyse/field/list/" + str(app.id))


@csrf_exempt
@login_required
def field_change_index(request, field_id, new_index):
    """
    修改字段排序编号
    :param request:
    :param field_id: 字段编号
    :param new_index: 新的排序编号
    :return: 是否修改成功
    """
    try:
        with transaction.atomic():
            field = Field.objects.get(id=field_id, is_delete=False)
            old_index = field.order_index
            field.order_index = new_index

            # 把新排序位置和老排序位置之间的字段签移
            if old_index < new_index:
                Field.objects.filter(order_index__gt=old_index, order_index__lte=new_index, app=field.app)\
                    .update(order_index=F('order_index') - 1)
            else:
                Field.objects.filter(order_index__gte=new_index, order_index__lt=old_index, app=field.app) \
                    .update(order_index=F('order_index') + 1)
            field.save()
    except IntegrityError:
        return HttpResponse("false")
    return HttpResponse("true")
