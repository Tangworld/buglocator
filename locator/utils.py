from locator import models
import time

def get_reports(status, assignee=''):
    reports = []
    if assignee == '':
        reports = models.Report.objects.filter(status=status)
    else:
        reports = models.Report.objects.filter(assignee=assignee, status=status)
    return reports


def get_all_reports():
    reports = models.Report.objects.all()
    return reports


def get_one_report(bugid):
    bug = models.Report.objects.filter(bugid=bugid)[0]
    productname = models.Product.objects.get(id=bug.productid).name
    bug.productid = productname
    open_local = time.localtime(float(bug.opendate))
    open_date = time.strftime("%Y-%m-%d %H:%M:%S", open_local)
    fix_local = time.localtime(float(bug.fixdate))
    fix_date = time.strftime("%Y-%m-%d %H:%M:%S", fix_local)
    bug.opendate = open_date
    bug.fixdate = fix_date

    return bug


def get_value(request, method, key):
    value = ''
    if method == 'session':
        value = request.session[key]
    if method == 'get':
        value = request.GET.get(key)
    if method == 'post':
        value = request.POST.get(key)
    return value


def get_lastpage(request):
    fullpath = request.get_full_path()
    request.session['lastpage'] = fullpath
