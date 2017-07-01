from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
]