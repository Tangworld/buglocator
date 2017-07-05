#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from locator import models

# Create your views here.


def index(request):
    """
    系统启动入口
    :param request: 
    :return: 进入登录页面
    """
    return render(request, 'login.html', )


def login(request):
    """
    登录验证方法，若通过验证则进入主页，否则返回登录页面并显示提示信息
    :param request: 
    :return: 
    """
    #if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    validate = {}
    v1 = ""
    v2 = ""
    flag = True
    validatepassword = ""
    username = ""
    password = ""

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    try:
        validatepassword = models.User.objects.get(username=username)
        if validatepassword.password != password:
            v2 = "密码错误！"
            flag = False
        print validatepassword
    except Exception, e:
        v2 = "密码错误！"
        flag = False

    if username == "":
        v1 = "用户名不能为空！"
        flag = False
    if password == "":
        v2 = "密码不能为空！"
        flag = False
    validate = {"v1": v1, "v2": v2}


    if flag:
        request.session["username"] = username
        request.session["password"] = password
        request.session['email'] = validatepassword.email
        return render(request, 'index.html')
    else:
        return render(request, 'login.html', {"validate": validate})


def logout(request):
    """
    退出方法，删除当前用户的session并返回登录页面
    :param request: 
    :return: 登录页面
    """
    del request.session['username']  # 删除session
    del request.session['password']
    return HttpResponseRedirect('/locator/index/')


def profile(request):
    """
    进入个人信息页面
    :param request: 
    :return: 个人信息页面
    """
    #if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    return render(request, 'profile.html')


def main(request):
    """
    由于login方法中涉及session操作，重复调用会导致错误，
    因此用这个方法作为系统内部进入主页的接口
    :param request: 
    :return: 进入主页
    """
    #if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    return render(request, 'index.html')


def edit(request):
    """
    进入编辑新密码页面
    :param request: 
    :return: 
    """
    #if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')

    return render(request, 'editprofile.html')


def confirm(request):
    """
    修改密码
    :param request: 
    :return: 
    """
    #if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    flag = True
    infomation = ""
    username = request.session['username']
    inputPassword = request.POST.get('password', None)
    inputPassword2 = request.POST.get('password2', None)
    if inputPassword == "":
        flag = False
        infomation = "密码不能为空！"
    if inputPassword2 == "":
        flag = False
        infomation = "确认密码不能为空！"
    if inputPassword != inputPassword2:
        flag = False
        infomation = "两次密码不一致！"
    if flag:
        user = models.User.objects.get(username=username)  # 查询该条记录
        user.password = inputPassword  # 修改
        user.save()
        return render(request, 'profile.html', {'success': '修改成功！'})
    else:
        return render(request, 'editprofile.html', {'infomation': infomation})


def lock(request):
    """
    锁定页面
    :param request: 
    :return: 
    """
    request.session['lock'] = 'lock'
    return render(request, 'lock_screen.html')


def unlock(request):
    """
    解锁页面
    :param request: 
    :return: 
    """
    request.session['lock'] = 'unlock'
    password = request.POST.get('password', None)
    realpassword = request.session['password']
    if password == realpassword:
        return HttpResponseRedirect('/locator/main/')
    else:
        return render(request, 'lock_screen.html')\

def authority(request):
    username = ""
    lock = request.session['lock']
    if lock == 'lock':
        return False
    else:
        return True
