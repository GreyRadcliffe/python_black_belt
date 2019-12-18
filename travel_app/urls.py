from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('travels/', views.travels),
    path('travels/add/', views.addTrip),
    path('travels/destination/<int:x>/', views.showTrip),
    path('travels/join/<int:x>/', views.joinTrip)
]