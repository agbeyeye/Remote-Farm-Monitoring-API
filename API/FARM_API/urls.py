from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [ 
    path('',views.homeView),
    path('login/', views.Login),
    path('request/', views.DataToRemoteDevice),
    url(r'^data/(?P<username>[-\w\_\d]+)/$', views.DataToRemoteDevice),
    path('alarms/', views.send_notification),
    path('alarm_ack/', views.alarm_acknowledgement),
    path('updateDataDevice/', views.updateDeviceDataModel),
    path('cropdata/', views.crop_info),
    path('api/data/', views.chartView,name = "chart-view"),
    url(r'^api/data/(?P<devicename>[-\w\ \_\d]+)/$', views.chartView),
]