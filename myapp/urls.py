from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_page),
    path('tour_agregator/', views.get_tour),
    path('info/', views.info),
    path('tours/', views.tours),
    path('login/', views.login),
]





