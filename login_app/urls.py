from . import views
from django.urls import path
from todo.views import TodoCreate

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_confirm, name='logout_confirm'),
    path('create/', TodoCreate.as_view(), name='todo_create'),
]