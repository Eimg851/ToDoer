from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('postLogin', views.postLogin, name='postLogin'),
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('signUp', views.signUp, name='signUp'),
    path('postSignUp', views.postSignUp, name="postSignUp"),
    path('postAddTask', views.postAddTask, name='postAddTask'),
    path('deleteTask', views.deleteTask, name='deleteTask'),
    path('markAsDone', views.markAsDone, name="markAsDone"),
    path('editTask', views.editTask, name="editTasks"),
    path('searchDB', views.search, name="searchDB"),
    path('clearSearch', views.clearSearch, name="clearSearch"),
    path('shareTask', views.shareTask, name="shareTask"),
    path('shareEntireList', views.shareEntireList, name="shareEntireList"),
    path('settings', views.settings, name="settings"),

]
