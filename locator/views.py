#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from locator import models

# Create your views here.

def index(request):
    return render(request, 'login.html', )

def login(request):
    validate = {}
    v1 = ""
    v2 = ""
    flag = True
    validatepassword = ""

    if request.method == "POST":
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
        return render(request, 'index.html')
    else:
        return render(request, 'login.html', {"validate": validate})

def logout(request):
    del request.session['username']  # 删除session
    del request.session['password']
    return HttpResponseRedirect('/locator/index/')
