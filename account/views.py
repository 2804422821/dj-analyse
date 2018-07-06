from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import RegisterForm


def account_login(request):
    """
    用户登录
    """
    if request.method == 'GET':
        if request.GET.get('next', None):
            return render(request, "login.html", {"next": request.GET["next"]})
        return render(request, "login.html", {"next": ''})
    else:
        username = request.POST["account"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if not request.POST.get('remember_me', None):
            #     request.session.set_expiry(0)
            request.session['theme'] = '我喜欢白色的主题'
            if request.POST.get('next', None):
                return redirect(request.POST["next"])
            return redirect("/account/profile")
        else:
            return render(request, "login.html", {'errorMsg': '登录失败，用户名或者密码错误'})


def account_profile(request):
    """
    用户信息
    """
    theme = request.session['theme']
    return render(request, "profile.html", {'theme': theme})


@csrf_exempt
def account_username_not_exists(request):
    """
    判断用户名是否不存在
    """
    username = request.POST["username"]
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("true")
    return HttpResponse("false")


@csrf_exempt
def account_email_not_exists(request):
    """
    判断用户邮箱是否不存在
    """
    email = request.POST["email"]
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("true")
    return HttpResponse("false")


def register(request):
    """
    用户注册
    """
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_user = register_form.save(commit=False)
            register_user.set_password(register_form.cleaned_data["password_confirm"])
            register_user.save()
            return redirect("/account/login")
        else:
            return render(request, "login.html", {'errorMsg': '注册失败'})

