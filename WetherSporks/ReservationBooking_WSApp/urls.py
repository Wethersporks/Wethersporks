"""
URL configuration for WetherSporks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .reservation_booker import views as online_res_booker_views
from .reservation_viewer import views as waitstaff_res_viewer_views


urlpatterns = [
    # ONLINE BOOKING URLS
    path("book/", online_res_booker_views.reservation_selector, name='booking'),
    path("book/cancel/<int:resID>", online_res_booker_views.reservation_deleter),


    # WAITSTAFFS VIEWER URLS
    path("view/TimeslotGenerator", waitstaff_res_viewer_views.timeslot_generator),
    path("view/dashboard", waitstaff_res_viewer_views.dashboard, name='dashboard'),
    path("view/update/<int:resID>", waitstaff_res_viewer_views.reservation_updater),

    #WELCOME PAGES
    #path("welcome/", views.welcome, name='welcome'),
    #path("welcome/contactus/", views.contact, name='contact')

]
