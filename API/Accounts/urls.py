from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [ 
    path('',views.homeView),
    path('dashboard',views.farmerDashboard, name= "farmer-dashboard"),
    path('login',views.login, name= "farmer-login"),
    path('api/data/', views.chartView,name = "chart-view"),
    path('api/valuestatus/', views.getDeviceValueStatus,name = "chart"),
    #url(r'^api/data/(?P<devicename>[-\w\ \_\d]+)/$', views.chartView),
]