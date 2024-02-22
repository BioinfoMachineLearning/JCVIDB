from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('details/<int:id>', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('registration/', views.create_User, name='registration'),
]