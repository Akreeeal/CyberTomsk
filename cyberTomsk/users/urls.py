from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'club'

urlpatterns=[
    path('login/', views.LoginUsers.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),

]