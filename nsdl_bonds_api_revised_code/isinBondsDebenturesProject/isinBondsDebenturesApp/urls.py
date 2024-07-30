from django.contrib import admin
from django.urls import path
from  .views import *

urlpatterns = [
    # path('<pan_number>/getIeccodeDetails/',GetIeccodeDetails.as_view(), name='GetIeccodeDetails'),
     path('<isin_number>/getIsinDetails/', getIsinDetails,name='getIsinDetails'),
     path('<path:invalid_path>', getCustom404View, name='invalid_path'),
]