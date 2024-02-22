from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('details/<int:id>', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('registration/', views.create_User, name='registration'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
]