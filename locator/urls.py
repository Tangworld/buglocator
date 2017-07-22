from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^main/$', views.main, name='main'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^lock/$', views.lock, name='lock'),
    url(r'^unlock/$', views.unlock, name='unlock'),
    url(r'^newreport/$', views.newreport, name='newreport'),
    url(r'^savereport/$', views.savereport, name='savereport'),
    url(r'^unfixed/$',views.unfixed,name='unfixed'),
    url(r'^fixed/$', views.fixed, name='fixed'),
    url(r'^show_open_bug/$', views.show_open_bug, name='show_open_bug'),
    url(r'^show_fixed_bug/$', views.show_fixed_bug, name='show_fixed_bug'),

    url(r'^index_admin/$', views.login, name='index_admin'),
    url(r'^profile_admin/$', views.profile, name='profile_admin'),
    url(r'^fixed_admin$', views.fixed, name='fixed_admin'),
    url(r'^unfixed_admin$', views.unfixed, name='unfixed_admin'),
    url(r'^not_assigned$', views.not_assigned, name='not_assigned'),
    url(r'^editprofile_admin$', views.edit, name='editprofile_admin'),

    url(r'^timeline$',views.more_timeline,name='timeline'),
    url(r'^timeline_admin$', views.more_timeline, name='timeline_admin'),
]