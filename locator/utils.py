from locator import models


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