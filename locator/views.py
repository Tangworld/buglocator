# -*- coding:utf-8 -*-

import random
import MySQLdb
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from locator import models
import time
import types
from domain import CurrentUser
from domain import Information
import json
from locator import utils
import test
import os
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
global pre_k_vocab
global pre_omega
global pre_phi
global pre_pl
global pre_ptw



def index(request):
    """
    系统启动入口
    :param request: 
    :return: 进入登录页面
    """
    utils.get_lastpage(request)
    return render(request, 'login.html', )


def login(request):
    """
    登录验证方法，若通过验证则进入主页，否则返回登录页面并显示提示信息
    :param request: 
    :return: 
    """
    utils.get_lastpage(request)
    v1 = ""
    v2 = ""
    flag = True
    validatepassword = ""

    username = utils.get_value(request, 'post', 'username')
    password = utils.get_value(request, 'post', 'password')
    try:
        validatepassword = models.User.objects.get(username=username)
        if validatepassword.password != password:
            v2 = "Incorrect password！"
            flag = False
    except Exception, e:
        print e
        v2 = "Incorrect password！"
        flag = False

    if username == "":
        v1 = "Username cannot be empty！"
        flag = False
    if password == "":
        v2 = "Password cannot be empty！"
        flag = False
    validate = {"v1": v1, "v2": v2}

    if flag:
        request.session["username"] = username
        request.session["password"] = password
        request.session['email'] = validatepassword.email
        request.session['userid'] = validatepassword.id
        request.session['isadmin'] = validatepassword.isadmin
        request.session['avatarloc'] = validatepassword.avatarloc

        if validatepassword.isadmin == 'yes':
            members = []
            dis_reports = []
            highdata = []
            circledata = []
            try:
                productobj = models.ProUser.objects.get(user_id=validatepassword.id)
                productId = int(productobj.product_id)
                userids = models.ProUser.objects.filter(product_id=productId)

                reports = utils.get_all_reports()
                for report in reports:
                    if report.status == 'fixed':
                        time_local = time.localtime(float(report.fixdate))
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        tmp = [dt, '2', report.bugid, report.summary, report.assignee, '1']
                        dis_reports.append(tmp)
                    elif report.status == 'unfixed':
                        time_local = time.localtime(float(report.opendate))
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        tmp = [dt, '3', report.bugid, report.summary, report.assignee, '0']
                        dis_reports.append(tmp)
                for report in reports:
                    time_local = time.localtime(float(report.opendate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if report.status == 'fixed':
                        tmp = [dt, '1', report.bugid, report.summary, report.reporter, '1']
                    elif report.status == 'unfixed':
                        tmp = [dt, '1', report.bugid, report.summary, report.reporter, '0']
                    else:
                        tmp = [dt, '1', report.bugid, report.summary, report.reporter, '2']
                    dis_reports.append(tmp)

                dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
                dis_content = []
                for i in range(len(dis_reports) - 1, len(dis_reports) - 16, -1):
                    if i >= 0:
                        dis_content.append(dis_reports[i])
                    else:
                        break

                for userid in userids:
                    one = models.User.objects.get(id=userid.user_id)
                    graph = models.Record.objects.get(userid=userid.user_id)
                    highdata.append({'name': one.username, 'data': [int(graph.b1), int(graph.b2), int(graph.b3), int(graph.b4), int(graph.b5), int(graph.b6), int(graph.b7)]})
                    circledata.append({'name': one.username,
                                       'y': int(graph.b1) + int(graph.b2) + int(graph.b3) + int(graph.b4) + int(graph.b5) +int(graph.b6) + int(graph.b7)})
                    member = {'id': one.id, 'username': one.username, 'email': one.email, 'mybugs': one.mybugs, 'isadmin': one.isadmin, 'avatar': one.avatarloc,
                              'b1': graph.b1, 'b2': graph.b2, 'b3': graph.b3, 'b4': graph.b4, 'b5': graph.b5, 'b6': graph.b6, 'b7': graph.b7,
                              'f1': graph.f1, 'f2': graph.f2, 'f3': graph.f3, 'f4': graph.f4, 'f5': graph.f5, 'f6': graph.f6, 'f7': graph.f7}
                    members.append(member)
            except Exception, e:
                print e

            return render(request, 'admin/index_admin.html', {'members': members, 'dis_reports': dis_content, 'series': json.dumps(highdata), 'data': json.dumps(circledata)})
        else:
            members = []
            dis_reports = []
            currentuser = CurrentUser()
            others = 0
            current = 0
            try:
                productobj = models.ProUser.objects.get(user_id=validatepassword.id)
                productId = int(productobj.product_id)
                userids = models.ProUser.objects.filter(product_id=productId)

                reports1 = models.Report.objects.filter(reporter=username)
                reports2 = models.Report.objects.filter(assignee=username)
                for report in reports1:
                    time_local = time.localtime(float(report.opendate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if report.status == 'fixed':
                        tmp = [dt, '1', report.bugid, report.summary, '1']
                    elif report.status == 'unfixed':
                        tmp = [dt, '1', report.bugid, report.summary, '0']
                    elif report.status == 'open':
                        tmp = [dt, '1', report.bugid, report.summary, '2']
                    dis_reports.append(tmp)
                for report in reports2:
                    if report.status == 'fixed':
                        time_local = time.localtime(float(report.fixdate))
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        tmp = [dt, '2', report.bugid, report.summary, '1']
                        dis_reports.append(tmp)
                    elif report.status == 'unfixed':
                        time_local = time.localtime(float(report.opendate))
                        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        tmp = [dt, '3', report.bugid, report.summary, '0']
                        dis_reports.append(tmp)
                dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
                dis_content = []
                for i in range(len(dis_reports) - 1, len(dis_reports) - 10, -1):
                    if i >= 0:
                        dis_content.append(dis_reports[i])
                    else:
                        break

                # 在构建members的同时将最近bugs数据加入进去
                #TODO 目前暂时默认取1到7月数据，若考虑真实应用场景还要结合当前日期进行修改。
                for userid in userids:
                    one = models.User.objects.get(id=userid.user_id)
                    graph = models.Record.objects.get(userid=userid.user_id)
                    member = {'id': one.id, 'username': one.username, 'email': one.email, 'mybugs': one.mybugs, 'isadmin': one.isadmin, 'avatar': one.avatarloc,
                              'b1': graph.b1, 'b2': graph.b2, 'b3': graph.b3, 'b4': graph.b4, 'b5': graph.b5, 'b6': graph.b6, 'b7': graph.b7,
                              'f1': graph.f1, 'f2': graph.f2, 'f3': graph.f3, 'f4': graph.f4, 'f5': graph.f5, 'f6': graph.f6, 'f7': graph.f7}
                    if int(userid.user_id) == int(validatepassword.id):
                        currentuser.setB(b1=graph.b1,b2=graph.b2,b3=graph.b3,b4=graph.b4,b5=graph.b5,b6=graph.b6,b7=graph.b7)
                        currentuser.setF(f1=graph.f1,f2=graph.f2,f3=graph.f3,f4=graph.f4,f5=graph.f5,f6=graph.f6,f7=graph.f7)
                        current += (int(graph.b1) + int(graph.b2) + int(graph.b3) + int(graph.b4) + int(graph.b5) + int(graph.b6) + int(graph.b7))
                    else:
                        others += (int(graph.b1) + int(graph.b2) + int(graph.b3) + int(graph.b4) + int(graph.b5) + int(graph.b6) + int(graph.b7))
                    members.append(member)
            except Exception, e:
                print e
            currentuser.setMyall(current)
            currentuser.setOthersall(others)

            return render(request, 'index.html', {'members': members, 'dis_reports': dis_content, 'currentuser': currentuser})
    else:
        return render(request, 'login.html', {"validate": validate})


def logout(request):
    """
    退出方法，删除当前用户的session并返回登录页面
    :param request: 
    :return: 登录页面
    """
    request.session.clear()  #直接清空session
    return HttpResponseRedirect('/locator/index/')


def profile(request):
    """
    进入个人信息页面
    :param request: 
    :return: 个人信息页面
    """
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)


    currentid = utils.get_value(request, 'session', 'userid')
    record = models.Record.objects.get(userid=currentid)
    maxvalue = 0
    minvalue = 1000
    maxmonth = ''
    minmonth = ''
    allbugs = 0
    allfiles =0
    allbugs = (int(record.b1)+int(record.b2)+int(record.b3)+int(record.b4)+int(record.b5)+int(record.b6)+int(record.b7))
    allfiles = (int(record.f1)+int(record.f2)+int(record.f3)+int(record.f4)+int(record.f5)+int(record.f6)+int(record.f7))
    if int(record.b1) > maxvalue:
        maxvalue = int(record.b1)
        maxmonth = 'January'
    if int(record.b1) < minvalue:
        minvalue = int(record.b1)
        minmonth = 'January'

    if int(record.b2) > maxvalue:
        maxvalue = int(record.b2)
        maxmonth = 'February'
    if int(record.b2) < minvalue:
        minvalue = int(record.b2)
        minmonth = 'February'

    if int(record.b3) > maxvalue:
        maxvalue = int(record.b3)
        maxmonth = 'March'
    if int(record.b3) < minvalue:
        minvalue = int(record.b3)
        minmonth = 'March'

    if int(record.b4) > maxvalue:
        maxvalue = int(record.b4)
        maxmonth = 'April'
    if int(record.b4) < minvalue:
        minvalue = int(record.b4)
        minmonth = 'April'

    if int(record.b5) > maxvalue:
        maxvalue = int(record.b5)
        maxmonth = 'May'
    if int(record.b5) < minvalue:
        minvalue = int(record.b5)
        minmonth = 'May'

    if int(record.b6) > maxvalue:
        maxvalue = int(record.b6)
        maxmonth = 'June'
    if int(record.b6) < minvalue:
        minvalue = int(record.b6)
        minmonth = 'June'

    if int(record.b7) > maxvalue:
        maxvalue = int(record.b7)
        maxmonth = 'July'
    if int(record.b7) < minvalue:
        minvalue = int(record.b7)
        minmonth = 'July'

    print minvalue
    print minmonth
    information = Information()
    information.setAll(allbugs=allbugs, allfiles=allfiles, maxmonth=maxmonth, minmonth=minmonth, b1=int(record.b1), b2=int(record.b2), b3=int(record.b3), b4=int(record.b4), b5=int(record.b5), b6=int(record.b6), b7=int(record.b7),
                      f1=int(record.f1), f2=int(record.f2), f3=int(record.f3), f4=int(record.f4), f5=int(record.f5), f6=int(record.f6), f7=int(record.f7))

    if utils.get_value(request, 'session', 'isadmin') == 'yes':
        return render(request, 'admin/profile_admin.html')
    else:
        return render(request, 'profile.html', {'infomation': information})


def main(request):
    """
    由于login方法中涉及session操作，重复调用会导致错误，
    因此用这个方法作为系统内部进入主页的接口
    :param request: 
    :return: 进入主页
    """
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    if utils.get_value(request, 'session', 'isadmin') == 'yes':
        members = []
        dis_reports = []
        highdata = []
        circledata = []
        try:
            productobj = models.ProUser.objects.get(user_id=utils.get_value(request, 'session', 'userid'))
            productId = int(productobj.product_id)
            userids = models.ProUser.objects.filter(product_id=productId)

            reports = utils.get_all_reports()
            for report in reports:
                if report.status == 'fixed':
                    time_local = time.localtime(float(report.fixdate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    tmp = [dt, '2', report.bugid, report.summary, report.assignee, '1']
                    dis_reports.append(tmp)
                elif report.status == 'unfixed':
                    time_local = time.localtime(float(report.opendate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    tmp = [dt, '3', report.bugid, report.summary, report.assignee, '0']
                    dis_reports.append(tmp)
            for report in reports:
                time_local = time.localtime(float(report.opendate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                if report.status == 'fixed':
                    tmp = [dt, '1', report.bugid, report.summary, report.reporter, '1']
                elif report.status == 'unfixed':
                    tmp = [dt, '1', report.bugid, report.summary, report.reporter, '0']
                else:
                    tmp = [dt, '1', report.bugid, report.summary, report.reporter,'2']
                dis_reports.append(tmp)

            dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
            dis_content = []
            for i in range(len(dis_reports) - 1, len(dis_reports) - 16, -1):
                if i >= 0:
                    dis_content.append(dis_reports[i])
                else:
                    break

            for userid in userids:
                one = models.User.objects.get(id=userid.user_id)
                graph = models.Record.objects.get(userid=userid.user_id)
                highdata.append({'name': one.username,
                                 'data': [int(graph.b1), int(graph.b2), int(graph.b3), int(graph.b4), int(graph.b5),
                                          int(graph.b6), int(graph.b7)]})
                circledata.append({'name': one.username,
                                    'y': int(graph.b1)+int(graph.b2)+int(graph.b3)+int(graph.b4)+int(graph.b5)+
                                          int(graph.b6)+int(graph.b7)})
                member = {'id': one.id, 'username': one.username, 'email': one.email, 'mybugs': one.mybugs,
                          'isadmin': one.isadmin, 'avatar': one.avatarloc,
                          'b1': graph.b1, 'b2': graph.b2, 'b3': graph.b3, 'b4': graph.b4, 'b5': graph.b5,
                          'b6': graph.b6, 'b7': graph.b7,
                          'f1': graph.f1, 'f2': graph.f2, 'f3': graph.f3, 'f4': graph.f4, 'f5': graph.f5,
                          'f6': graph.f6, 'f7': graph.f7}
                members.append(member)
        except Exception, e:
            print e

        return render(request, 'admin/index_admin.html', {'members': members, 'dis_reports': dis_content, 'series': json.dumps(highdata), 'data': json.dumps(circledata)})
    else:
        members = []
        dis_reports = []
        currentuser = CurrentUser()
        others = 0
        current = 0
        try:
            productobj = models.ProUser.objects.get(user_id=utils.get_value(request, 'session', 'userid'))
            productId = int(productobj.product_id)
            userids = models.ProUser.objects.filter(product_id=productId)

            reports1 = models.Report.objects.filter(reporter=utils.get_value(request, 'session', 'username'))
            reports2 = models.Report.objects.filter(assignee=utils.get_value(request, 'session', 'username'))
            for report in reports1:
                time_local = time.localtime(float(report.opendate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                if report.status == 'fixed':
                    tmp = [dt, '1', report.bugid, report.summary, '1']
                elif report.status == 'unfixed':
                    tmp = [dt, '1', report.bugid, report.summary, '0']
                elif report.status == 'open':
                    tmp = [dt, '1', report.bugid, report.summary, '2']
                dis_reports.append(tmp)
            for report in reports2:
                if report.status == 'fixed':
                    time_local = time.localtime(float(report.fixdate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    tmp = [dt, '2', report.bugid, report.summary, '1']
                    dis_reports.append(tmp)
                elif report.status == 'unfixed':
                    time_local = time.localtime(float(report.opendate))
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    tmp = [dt, '3', report.bugid, report.summary, '0']
                    dis_reports.append(tmp)
            dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
            dis_content = []
            for i in range(len(dis_reports) - 1, len(dis_reports) - 10, -1):
                if i >= 0:
                    dis_content.append(dis_reports[i])
                else:
                    break
            for userid in userids:
                one = models.User.objects.get(id=userid.user_id)
                graph = models.Record.objects.get(userid=userid.user_id)
                member = {'id': one.id, 'username': one.username, 'email': one.email, 'mybugs': one.mybugs,
                          'isadmin': one.isadmin, 'avatar': one.avatarloc,
                          'b1': graph.b1, 'b2': graph.b2, 'b3': graph.b3, 'b4': graph.b4, 'b5': graph.b5,
                          'b6': graph.b6, 'b7': graph.b7,
                          'f1': graph.f1, 'f2': graph.f2, 'f3': graph.f3, 'f4': graph.f4, 'f5': graph.f5,
                          'f6': graph.f6, 'f7': graph.f7}
                if int(userid.user_id) == int(request.session['userid']):
                    currentuser.setB(b1=graph.b1, b2=graph.b2, b3=graph.b3, b4=graph.b4, b5=graph.b5, b6=graph.b6,
                                     b7=graph.b7)
                    currentuser.setF(f1=graph.f1, f2=graph.f2, f3=graph.f3, f4=graph.f4, f5=graph.f5, f6=graph.f6,
                                     f7=graph.f7)
                    current += (
                    int(graph.b1) + int(graph.b2) + int(graph.b3) + int(graph.b4) + int(graph.b5) + int(graph.b6) + int(
                        graph.b7))
                else:
                    others += (
                    int(graph.b1) + int(graph.b2) + int(graph.b3) + int(graph.b4) + int(graph.b5) + int(graph.b6) + int(
                        graph.b7))
                members.append(member)
        except Exception, e:
            print e
        currentuser.setMyall(current)
        currentuser.setOthersall(others)

        return render(request, 'index.html', {'members': members, 'dis_reports': dis_content, 'currentuser': currentuser})


def edit(request):
    """
    进入编辑新密码页面
    :param request: 
    :return: 
    """
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    if utils.get_value(request, 'session', 'isadmin') == 'yes':
        return render(request, 'admin/editprofile_admin.html')
    else:
        return render(request, 'editprofile.html')


def confirm(request):
    """
    修改密码
    :param request: 
    :return: 
    """
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    flag = True
    infomation = ""
    username = utils.get_value(request, 'session', 'username')
    inputPassword = utils.get_value(request, 'post', 'password')
    inputPassword2 = utils.get_value(request, 'post', 'password2')
    if inputPassword == "":
        flag = False
        infomation = "Password cannot be empty！"
    if inputPassword2 == "":
        flag = False
        infomation = "Confirm cannot be empty！"
    if inputPassword != inputPassword2:
        flag = False
        infomation = "Password and confirm password must be consistent!"
    if flag:
        user = models.User.objects.get(username=username)  # 查询该条记录
        user.password = inputPassword  # 修改
        user.save()
        return render(request, 'profile.html', {'success': 'Success！'})
    else:
        return render(request, 'editprofile.html', {'infomation': infomation})


def lock(request):
    """
    锁定页面
    :param request: 
    :return: 
    """
    utils.get_lastpage(request)
    request.session['lock'] = 'lock'
    return render(request, 'lock_screen.html')


def unlock(request):
    """
    解锁页面
    先判断输入的密码是否正确，若正确进入主页的同时删除session中的lock值，否则返回锁定页面
    :param request: 
    :return: 
    """
    password = utils.get_value(request, 'post', 'password')
    realpassword = utils.get_value(request, 'session', 'password')

    utils.get_lastpage(request)

    if password == realpassword:
        del request.session['lock']
        return HttpResponseRedirect('/locator/main/')
    else:
        return render(request, 'lock_screen.html')


def newreport(request):
    """
    跳转到提交报告页面（废弃）
    :param request: 
    :return: 
    """
    # authority(request)
    current = request.session['username']
    finalusers = []
    finalproducts = []
    products = models.Product.objects.all()
    for p in products:
        finalproducts.append(p.name)

    users = models.User.objects.all()
    for u in users:
        if u.username != current:
            finalusers.append(u.username)

    return render(request, 'newreport.html', {'products': finalproducts, 'users': finalusers})


def savereport(request):
    """
    存储新的缺陷报告（废弃）
    status 参数 ：open代表未分配，unfix代表未修复，fixed代表已修复
    :param request: 
    :return: 
    """
    # authority(request)
    summary = request.POST.get('summary')
    description = request.POST.get('description')
    reporter = request.session['userid']
    assignee = request.POST.get('assignee')
    productid = request.POST.get('product')
    status = 'open'
    opendate = time.strftime("%Y-%d-%m")
    component = request.POST.get('component')
    version = request.POST.get('version')
    platform = request.POST.get('platform')
    os = request.POST.get('os')
    priority = request.POST.get('priority')
    severity = request.POST.get('severity')

    models.Report.objects.create(summary=summary, description=description, reporter=reporter,
                                 assignee=assignee, status=status, opendate=opendate,
                                 component=component, version=version, platform=platform, os=os,
                                 priority=priority, severity=severity, productid=productid)
    return HttpResponseRedirect('/locator/main')



def unfixed(request):
    # 待修复页面
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    current_isadmin = utils.get_value(request, 'session', 'isadmin')
    current_username = utils.get_value(request, 'session', 'username')
    disContent = []

    if current_isadmin == 'yes':
        reports = utils.get_reports(status='open')
        for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), report.assignee)
            disContent.append(tmpContent)

        return render(request, 'admin/defects_not_resolved_admin.html', {'contents': disContent})
    else:
        reports = utils.get_reports(status='open', assignee=current_username)
        for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))))
            disContent.append(tmpContent)

        return render(request, 'defects_not_resolved.html', {'contents': disContent})


def fixed(request):
    # 已修复页面
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    current_isadmin = utils.get_value(request, 'session', 'isadmin')
    current_username = utils.get_value(request, 'session', 'username')
    disContent = []

    if current_isadmin == 'yes':
        reports = utils.get_reports('fixed')
        for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.fixdate))))
            disContent.append(tmpContent)

        return render(request, 'admin/defects_resolved_admin.html', {'contents': disContent})
    else:

        reports = utils.get_reports('fixed', current_username)
        for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.fixdate))))
            disContent.append(tmpContent)
        return render(request, 'defects_resolved.html', {'contents': disContent})


def not_assigned(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    disContent = []

    reports = utils.get_reports('open')

    for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(report.opendate))))
            disContent.append(tmpContent)
    return render(request, 'admin/defects_not_assigned_admin.html', {'contents': disContent})

def more_timeline(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    utils.get_lastpage(request)

    current_isadmin = utils.get_value(request, 'session', 'isadmin')
    current_username = utils.get_value(request, 'session', 'username')
    dis_reports = []

    if current_isadmin == 'yes':
        reports = utils.get_all_reports()
        #print len(reports)
        for report in reports:
            if report.status == 'fixed':
                time_local = time.localtime(float(report.fixdate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                tmp = [dt, '2', report.bugid, report.summary, report.assignee, '1']
                dis_reports.append(tmp)
            elif report.status == 'unfixed':
                time_local = time.localtime(float(report.opendate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                tmp = [dt, '3', report.bugid, report.summary, report.assignee, '0']
                dis_reports.append(tmp)
        for report in reports:
            time_local = time.localtime(float(report.opendate))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            if report.status == 'fixed':
                tmp = [dt, '1', report.bugid, report.summary, report.reporter, '1']
            elif report.status == 'unfixed':
                tmp = [dt, '1', report.bugid, report.summary, report.reporter, '0']
            else:
                tmp = [dt, '1', report.bugid, report.summary, report.reporter, '2']
            dis_reports.append(tmp)

        dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
        dis_content = []
        for i in range(len(dis_reports) - 1, -1, -1):
            dis_content.append(dis_reports[i])

        return render(request, 'admin/timeline_admin.html', {'dis_reports': dis_content})
    else:
        reports1 = models.Report.objects.filter(reporter=current_username)
        reports2 = models.Report.objects.filter(assignee=current_username)
        for report in reports1:
            time_local = time.localtime(float(report.opendate))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            if report.status == 'fixed':
                tmp = [dt, '1', report.bugid, report.summary,'1']
            elif report.status == 'unfixed':
                tmp = [dt, '1', report.bugid, report.summary, '0']
            else :
                tmp = [dt, '1', report.bugid, report.summary, '2']
            dis_reports.append(tmp)
        for report in reports2:
            if report.status == 'fixed':
                time_local = time.localtime(float(report.fixdate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                tmp = [dt, '2', report.bugid, report.summary, '1']
                dis_reports.append(tmp)
            elif report.status == 'unfixed':
                time_local = time.localtime(float(report.opendate))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                tmp = [dt, '3', report.bugid, report.summary, '0']
                dis_reports.append(tmp)
        dis_reports.sort(lambda x, y: cmp(x[0], y[0]))
        dis_content = []
        for i in range(len(dis_reports) - 1, -1, -1):
            dis_content.append(dis_reports[i])

        return render(request, 'timeline.html', {'dis_reports': dis_content})


def check_lock(request):
    '''
    若session里有lock这个值证明页面已经被锁定，解锁后删除session中相应值，因此若没有lock这个值证明未锁定
    :param request: 
    :return: 
    '''
    lock = 'lock' in request.session
    return lock


def authority(request):
    '''
    判断是否是登录状态
    :param request: 
    :return: 
    '''
    userflag = 'username' in request.session
    return userflag


def show_open_bug(request):
    '''
    展示open bug的具体信息
    :param request: open bug展示页面
    :return: 
    '''
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    premeter_to_memry(request)

    bugid = utils.get_value(request, 'get', 'bugid')
    flag = utils.get_value(request, 'get', 'flag')
    request.session['flag'] = flag
    bug = utils.get_one_report(bugid)
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/show_open_admin.html', {'bug': bug})
    else:
        return render(request, 'show_open_bug.html', {'bug': bug})


def show_fixed_bug(request):
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    bugid = utils.get_value(request, 'get', 'bugid')
    flag = utils.get_value(request, 'get', 'flag')
    request.session['flag'] = flag
    bug = utils.get_one_report(bugid)
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/show_fixed_admin.html', {'bug': bug})
    else:
        return render(request, 'show_fixed_bug.html', {'bug': bug})


def show_notassigned_bug(request):
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    bugid = utils.get_value(request, 'get', 'bugid')
    flag = utils.get_value(request, 'get', 'flag')
    request.session['flag'] = flag
    bug = utils.get_one_report(bugid)
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/show_notassigned_admin.html', {'bug': bug})
    else:
        return render(request, 'show_notassigned_bug.html', {'bug': bug})


def back(request):
    '''
    1：overview页面
    2：timeline页面
    3：open页面
    4：fixed页面
    5：notassigned页面
    解决进入具体页面后返回的路径
    :param request: 页面重定向
    :return: 
    '''
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    lastpage = utils.get_value(request, 'session', 'lastpage')
    print lastpage
    return HttpResponseRedirect(lastpage)


def alg_res(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')
    #原有代码
    pre = BASE_DIR+'/data/bughunter/'

    cList = [' ', '<', '>', '&', '\'', '"', '\n']
    cDict = {' ': '&nbsp;',
             '<': '&lt;',
             '>': '&gt;',
             '\'': '&apos;',
             '"': 'quot;',
             '\n': '<br>'}

    filelist = []
    bugid = utils.get_value(request, 'get', 'bugid')
    result = get_result(request, bugid)
    wordArr = []
    aWord = []
    # print result
    for r in result:
        filepath = models.filemap.objects.get(filenumber=r).filepath
        thispath = str(pre + filepath)
        try:
            thiscontent = open(thispath, 'r')
            fileStr = thiscontent.read()
            for char in fileStr:
                if char.isalpha():
                    aWord.append(char)
                elif char.isdigit():
                    aWord.append(char)
                else:
                    wordArr.append("".join(aWord))
                    aWord = []
                    if char not in cList:
                        wordArr.append(char)
                    else:
                        wordArr.append(cDict[char])
            filelist.append({'content': fileStr, 'path': filepath})

            # content.append(thiscontent.readlines())
        except Exception, e:
            print e

    #测试代码

    # testPath = '/home/ranger/PycharmProjects/new/buglocator/locator/urls.py'
    # fileStr = open('/home/ranger/PycharmProjects/new/buglocator/locator/another.txt', 'r').read()
    # fileTest = open(testPath,'r').read()
    #
    # for char in fileStr:
    #     if char.isalpha():
    #         aWord.append(char)
    #     elif char.isdigit():
    #         aWord.append(char)
    #     else:
    #         wordArr.append("".join(aWord))
    #         aWord = []
    #         if char not in cList:
    #             wordArr.append(char)
    #         else:
    #             wordArr.append(cDict[char])
    kwArr = ['applet', 'RPFactor', 'RemoteUIApplet', 'class']
    # paths.append('/home/tsj/PycharmProjects/buglocator/locator/models.py')
    # file = open('/home/tsj/PycharmProjects/buglocator/locator/models.py', 'r')
    # content.append(file.read())
    # return render(request, 'resultPage.html', {'fileArr':json.dumps(wordArr), 'sel_arr':json.dumps(kwArr),
    #                                            'path':testPath,'file':fileTest})
    return render(request, 'resultPage.html', {'fileArr':json.dumps(wordArr), 'sel_arr':json.dumps(kwArr), 'filelist': filelist, 'bugid': bugid})



def get_result(request, bugid):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    global pre_k_vocab
    global pre_omega
    global pre_phi
    global pre_pl
    global pre_ptw

    # 获取k_vocab参数
    # print pre_k_vocab
    r_k_vocab = eval(pre_k_vocab[0])
    # 获取omega参数
    r_omega = eval(pre_omega[0])
    # 获取phi参数
    r_phi = eval(pre_phi[0])
    # 获取pl参数
    r_pl = eval(pre_pl[0])
    r_ptw = eval(pre_ptw[0])

    indexx = models.bugidmap.objects.get(bugid=bugid).bugidnumber
    current_report = models.reports.objects.get(reportnumber=indexx).content

    current_report = eval(current_report)
    ws = current_report[1]
    ts = current_report[0]
    # print type(ws), type(ts)
    # print ws, ts
    report = {'ws': ws, 'ts': ts}


    result = []
    s_ptd = test.llda_test(report, r_k_vocab, r_pl, r_phi, r_omega, r_ptw)
    for i in range(0, 10):
        result.append(s_ptd[i][0])
    return result



def cloud(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    return render(request, 'cloud.html')

def premeter_to_memry(request):
    k_vocab = open(BASE_DIR + '/data/bughunter/k_vocab.txt', 'r')
    omega = open(BASE_DIR + '/data/bughunter/omega.txt', 'r')
    phi = open(BASE_DIR + '/data/bughunter/phi.txt', 'r')
    pl = open(BASE_DIR + '/data/bughunter/pl.txt', 'r')
    ptw = open(BASE_DIR + '/data/bughunter/ptw.txt', 'r')

    global pre_k_vocab
    global pre_omega
    global pre_phi
    global pre_pl
    global pre_ptw

    pre_k_vocab = k_vocab.readlines()
    pre_omega = omega.readlines()
    pre_phi = phi.readlines()
    pre_pl = pl.readlines()
    pre_ptw = ptw.readlines()

    k_vocab.close()
    omega.close()
    phi.close()
    pl.close()
    ptw.close()
    # return pre_k_vocab, pre_omega, pre_phi, pre_pl, pre_ptw

def save_assignment(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    assignee = request.POST.get('assignee')
    bugid = request.POST.get('bugid')
    bug = models.Report.objects.filter(bugid=bugid)[0]
    bug.assignee = assignee
    bug.save()
    return HttpResponseRedirect('/locator/not_assigned')

def to_fix(request):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    bugid = request.POST.get('bugid')
    print bugid
    report = models.Report.objects.get(bugid=bugid)
    report.status = 'fix'
    report.save()
    return HttpResponseRedirect('/locator/unfix')
