from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.sign_up, name='sign_up'),
    path('verify/', views.verify, name='verify'),
]