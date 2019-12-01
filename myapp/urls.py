from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home_page),
    url(r'search.php?\w+', views.home_page),
    path('info/', views.info),
    path('tours/', views.tours),
    path('index/', views.index),
    url(r'index/register/$', views.RegisterFormView.as_view()),
    url(r'index/login/$', views.LoginFormView.as_view()),
    url(r'index/logout/$', views.LogoutView.as_view()),
    url(r'index/password-change/', views.PasswordChangeView.as_view())
]
