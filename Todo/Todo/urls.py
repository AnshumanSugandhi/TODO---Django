# Todo/Todo/urls.py
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('todo/', views.TodoList , name='todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('logout/', views.Logout, name='logout'),]
