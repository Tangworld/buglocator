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
import os
import pickle

import test
import L2ss
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

global r_k_vocab
global r_phi
global r_pl
global r_ptw
global r_pws
global kwArr
global all_cloud



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

    # print minvalue
    # print minmonth
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
        return HttpResponseRedirect('/locator/profile/')
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
        reports = utils.get_reports(status='unfixed')
        for report in reports:
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), report.assignee)
            disContent.append(tmpContent)

        return render(request, 'admin/defects_not_resolved_admin.html', {'contents': disContent})
    else:
        reports = utils.get_reports(status='unfixed', assignee=current_username)
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


    bugid = utils.get_value(request, 'get', 'bugid')
    bug = utils.get_one_report(bugid)
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/show_open_admin.html', {'bug': bug})
    else:
        # premeter_to_memry(request)
        return render(request, 'show_open_bug.html', {'bug': bug})


def show_fixed_bug(request):
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    bugid = utils.get_value(request, 'get', 'bugid')
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
    bug = utils.get_one_report(bugid)
    if request.session['isadmin'] == 'yes':
        productobj = models.ProUser.objects.get(user_id=utils.get_value(request, 'session', 'userid'))
        productId = int(productobj.product_id)
        userids = models.ProUser.objects.filter(product_id=productId)
        users = []
        for userid in userids:
            one = models.User.objects.get(id=userid.user_id)
            if not one.username == 'Admin':
                users.append(one.username)
        return render(request, 'admin/show_notassigned_admin.html', {'bug': bug, 'users': users})
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
    # print lastpage
    return HttpResponseRedirect(lastpage)


def alg_res(request):
    global kwArr
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')
    methodid = request.GET.get('method')
    pre = BASE_DIR+'/data/bughunter/'
    '''
    cList = [' ', '<', '>', '\'', '"', '\n']
    cDict = {' ': '&nbsp;',
             '<': '&lt;',
             '>': '&gt;',
             '\'': '&apos;',
             '"': 'quot;',
             '\n': '<br>'}
    '''
    filelist = []
    bugid = utils.get_value(request, 'get', 'bugid')
    # print bugid
    result = get_result(request, bugid)
    # wordArr = []
    aWord = []
    # 以下对description内容进行切分
    bugreport = models.Report.objects.get(bugid=bugid).description
    '''
    for char in bugreport:
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
    '''
    # 以下读取结果中的文件内容并获取文件对应的关键词
    kwArr = []

    kwPos = []
    str_kws = []
    filename = []
    for r in result:
        str_kw = ''
        filepath = models.filemap.objects.get(filenumber=r).filepath
        tmp = filepath.strip().split('/')[-1][0:-5]
        filename.append(tmp)
        # print r
        keywordIDs = models.f2w.objects.get(fileID=r).keywords.split(' ')
        keywords = models.wordmap.objects.filter(wordID__in=keywordIDs[0:-1])
        for keyword in keywords:
            #tmp.append(keyword.word)
            kwArr.append(keyword.word)
            str_kw += (keyword.word+' ')
            # print tmp
        #kwArr.append(tmp)
        # print len(kwArr)
        thispath = str(pre + filepath)
        str_kws.append(str_kw)
        try:
            thiscontent = open(thispath, 'r')
            fileStr = thiscontent.read()
            filelist.append({'content': fileStr, 'path': filepath})
        except Exception, e:
            print e

    common = ''
    for kw in kwArr:
        if kwArr.count(kw) > 1:
            common += (kw + ' ')
    # print common
    str_kws.append(common)
    # 获取全部文件的关键词
    global all_cloud
    all_cloud = []
    temp = []
    lower_report = bugreport.lower()
    for kw in kwArr:
        if kw in bugreport:
            temp.append({'word': kw, 'time': lower_report.count(kw)})
    for t in temp:
        if t not in all_cloud:
            all_cloud.append(t)
    return render(request, 'resultPage.html', {'sel_arr': kwArr, 'str_kws': str_kws,'method': methodid,'filename':filename,
                                               'filelist': filelist, 'bugid': bugid, 'report': bugreport})


def get_result(request, bugid):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    start = time.time()
    global r_k_vocab
    global r_phi
    global r_pl
    global r_ptw
    global r_pws

    indexx = models.bugidmap.objects.get(bugid=bugid).bugidnumber
    current_report = models.reports.objects.get(reportnumber=indexx).content

    current_report = eval(current_report)
    ws = current_report[1]
    ts = current_report[0]
    # print type(ws), type(ts)
    # print ws, ts
    report = {'ws': ws, 'ts': ts}

    result = []
    #s_ptd = test.llda_test(report, r_k_vocab, r_pl, r_phi, r_omega, r_ptw, r_pws)
    s_ptd = test.llda_test(report, r_k_vocab, r_pl, r_phi, r_ptw, r_pws)
    for i in range(0, 15):
        result.append(s_ptd[i][0]+1)
    end = time.time()
    print "BugHunter consumed %f s."%(end-start)
    # print 'bughunter ', result
    return result


def alg_res_l2ss(request):
    global kwArr
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')
    methodid = request.GET.get('method')
    pre = BASE_DIR+'/data/bughunter/'
    '''
    cList = [' ', '<', '>', '\'', '"', '\n']
    cDict = {' ': '&nbsp;',
             '<': '&lt;',
             '>': '&gt;',
             '\'': '&apos;',
             '"': 'quot;',
             '\n': '<br>'}
    '''
    filelist = []
    bugid = utils.get_value(request, 'get', 'bugid')
    # print bugid
    result = get_result_l2ss(request, str(bugid))
    # wordArr = []
    # aWord = []
    # 以下对description内容进行切分
    bugreport = models.Report.objects.get(bugid=bugid).description
    # print 'report:>>>>>>', bugreport
    '''
    for char in bugreport:
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
    '''
    # 以下读取结果中的文件内容并获取文件对应的关键词



    kwArr = []
    str_kws = []
    filename = []
    for r in result:
        str_kw = ''
        # print r
        filepath = models.filemap.objects.get(path_l2ss=r).filepath
        tmp = filepath.strip().split('/')[-1][0:-5]
        filename.append(tmp)
        fileid = models.filemap.objects.get(path_l2ss=r).filenumber
        # print fileid
        keywordIDs = models.f2w.objects.get(fileID=fileid).keywords.split(' ')
        # print keywordIDs
        keywords = models.wordmap.objects.filter(wordID__in=keywordIDs[0:-1])
        # print keywords
        #tmp = []
        for keyword in keywords:
            #tmp.append(keyword.word)
            kwArr.append(keyword.word)
            str_kw += (keyword.word + ' ')
            # print tmp
        # kwArr.append(tmp)
        # print 'len:::::', len(kwArr)
        thispath = str(pre + filepath)
        str_kws.append(str_kw)
        try:
            thiscontent = open(thispath, 'r')
            fileStr = thiscontent.read()
            filelist.append({'content': fileStr, 'path': filepath})
        except Exception, e:
            print e
    common = ''
    for kw in kwArr:
        if kwArr.count(kw) > 1:
            common += (kw + ' ')
    #print common
    str_kws.append(common)

    # 获取全部文件的关键词
    global all_cloud
    all_cloud = []
    temp = []
    lower_report = bugreport.lower()
    for kw in kwArr:
        if kw in bugreport:
            temp.append({'word': kw, 'time': lower_report.count(kw)})
    for t in temp:
        if t not in all_cloud:
            all_cloud.append(t)
    return render(request, 'resultPage.html', {'sel_arr': kwArr, 'str_kws': str_kws, 'filename':filename,
                'filelist': filelist, 'bugid': bugid, 'report': bugreport, 'method':methodid})


def get_result_l2ss(request, bugid):
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')
    start = time.time()
    pkl_aspectj_l2ss = file(BASE_DIR+'/data/L2SS/aspectj.pkl', 'rb')
    pkl_epl_l2ss = file(BASE_DIR+'/data/L2SS/epl_l2ss.pkl', 'rb')
    pkl_phi2_l2ss = file(BASE_DIR + '/data/L2SS/phi2_l2ss.pkl', 'rb')
    pkl_phi_l2ss = file(BASE_DIR + '/data/L2SS/phi_l2ss.pkl', 'rb')
    pkl_pl_l2ss = file(BASE_DIR + '/data/L2SS/pl_l2ss.pkl', 'rb')
    pkl_ptw_l2ss = file(BASE_DIR + '/data/L2SS/ptw_l2ss.pkl', 'rb')
    pkl_tr_dis_l2ss = file(BASE_DIR + '/data/L2SS/tr_dis_l2ss.pkl', 'rb')

    data_l2ss = pickle.load(pkl_aspectj_l2ss)
    epl_l2ss = pickle.load(pkl_epl_l2ss)
    phi_l2ss = pickle.load(pkl_phi_l2ss)
    phi2_l2ss = pickle.load(pkl_phi2_l2ss)
    pl_l2ss = pickle.load(pkl_pl_l2ss)
    ptw_l2ss = pickle.load(pkl_ptw_l2ss)
    tr_dis_l2ss = pickle.load(pkl_tr_dis_l2ss)

    pkl_aspectj_l2ss.close()
    pkl_epl_l2ss.close()
    pkl_phi2_l2ss.close()
    pkl_phi_l2ss.close()
    pkl_pl_l2ss.close()
    pkl_ptw_l2ss.close()
    pkl_tr_dis_l2ss.close()

    s_ptd = L2ss.l2ss_test(bugid, epl_l2ss, pl_l2ss, phi_l2ss, phi2_l2ss, ptw_l2ss, tr_dis_l2ss, data_l2ss)
    result = []
    for i in range(15):
        result.append(s_ptd[i][0])
    end = time.time()
    print "L2SS consumed %f s." %(end - start)
    # print 'l2ss: ', result
    return result


def cloud(request):
    global kwArr
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)

    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')

    global all_cloud
    all_kw = []
    all_tm = []
    for a in all_cloud:
        all_kw.append(a['word'])
        all_tm.append(a['time'])
    # print all_kw
    # print all_tm

    # Type = int(request.GET.get('type'))
    # print type(Type)
    # if Type != 10:
    #     keywords = kwArr[Type * 20:(Type + 1) * 20]
    #     print keywords
    # else:
    #     keywords = []
    return render(request, 'static_cloud.html', {'keywords': json.dumps(all_kw), 'times': json.dumps(all_tm)})


def premeter_to_memry(request):
    pkl_k_vocab = file(BASE_DIR+'/data/bughunter/k_vocab.pkl', 'rb')
    pkl_phi = file(BASE_DIR+'/data/bughunter/phi.pkl', 'rb')
    pkl_pl = file(BASE_DIR+'/data/bughunter/pl.pkl', 'rb')
    pkl_ptw = file(BASE_DIR+'/data/bughunter/ptw.pkl', 'rb')
    pkl_pws = file(BASE_DIR+'/data/bughunter/pws.pkl', 'rb')

    global r_k_vocab
    global r_phi
    global r_pl
    global r_ptw
    global r_pws

    r_k_vocab = pickle.load(pkl_k_vocab)
    r_phi = pickle.load(pkl_phi)
    r_pl = pickle.load(pkl_pl)
    r_ptw = pickle.load(pkl_ptw)
    r_pws = pickle.load(pkl_pws)

    pkl_k_vocab.close()
    pkl_phi.close()
    pkl_pl.close()
    pkl_ptw.close()
    pkl_pws.close()


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
    bug.status = 'unfixed'
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

    bugid = utils.get_value(request, 'post', 'bugid')
    timestamp = int(time.time())
    # print type(bugid)
    # print bugid
    # print timestamp
    report = models.Report.objects.get(bugid=bugid)
    report.status = 'fixed'
    report.fixdate = timestamp
    report.save()
    return HttpResponseRedirect('/locator/unfixed')

def mix(request):
    global kwArr
    # 权限控制
    lockflag = check_lock(request)
    userflag = authority(request)
    if lockflag:
        return HttpResponseRedirect('/locator/lock/')
    if not userflag:
        return HttpResponseRedirect('/locator/index/')
    methodid = request.GET.get('method')
    pre = BASE_DIR + '/data/bughunter/'

    filelist = []
    bugid = utils.get_value(request, 'get', 'bugid')

    # 拿到了两种方法定位的结果
    result_bh = get_result(request, bugid)
    result_l2ss = get_result_l2ss(request, str(bugid))
    bugreport = models.Report.objects.get(bugid=bugid).description


    kwArr = []
    str_kws = []
    filename = []
    real_result = []
    # 拿到两种方法的公共文件
    for rl in result_l2ss:
        filenumber = models.filemap.objects.get(path_l2ss=rl).filenumber
        filenumber = int(filenumber)
        if filenumber in result_bh:
            real_result.append(filenumber)

    # 开始对两种方法的公共结果进行处理
    for r in real_result:
        str_kw = ''
        filepath = models.filemap.objects.get(filenumber=r).filepath
        tmp = filepath.strip().split('/')[-1][0:-5]
        filename.append(tmp)
        # print r
        keywordIDs = models.f2w.objects.get(fileID=r).keywords.split(' ')
        keywords = models.wordmap.objects.filter(wordID__in=keywordIDs[0:-1])
        for keyword in keywords:
            #tmp.append(keyword.word)
            kwArr.append(keyword.word)
            str_kw += (keyword.word+' ')
            # print tmp
        #kwArr.append(tmp)
        # print len(kwArr)
        thispath = str(pre + filepath)
        str_kws.append(str_kw)
        try:
            thiscontent = open(thispath, 'r')
            fileStr = thiscontent.read()
            filelist.append({'content': fileStr, 'path': filepath})
        except Exception, e:
            print e

    common = ''
    for kw in kwArr:
        if kwArr.count(kw) > 1:
            common += (kw + ' ')
    # print common
    str_kws.append(common)
    # 获取全部文件的关键词
    global all_cloud
    all_cloud = []
    temp = []
    lower_report = bugreport.lower()
    for kw in kwArr:
        if kw in bugreport:
            temp.append({'word': kw, 'time': lower_report.count(kw)})
    for t in temp:
        if t not in all_cloud:
            all_cloud.append(t)
    # red #ff3778 #daafe8 #ffcccc yellow #9ad6fc #6265fe #339999 #99ccff #ccff99 #66cccc green blue #666699 #c0a16b
    color = ['red', '#ff3778', '#daafe8', '#ffcccc', 'yellow', '#9ad6fc', '#6265fe', '#339999', '#99ccff', '#ccff99', '#66cccc', 'green', 'blue', '#666699', '#c0a16b']
    display = zip(filename, color)
    return render(request, 'mix_resultPage.html', {'sel_arr': kwArr, 'str_kws': str_kws,'method': methodid,
                                               'filelist': filelist, 'bugid': bugid, 'report': bugreport, 'display': display})


def load(request):

    premeter_to_memry(request)
    return render(request, 'blank.html')
