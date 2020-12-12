from django.contrib import admin
from django.urls import path, include
from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', views.handleLogin, name='handleLogout'),
    path('logout', views.handleLogout, name='handleLogout'),
    

]



