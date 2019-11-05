from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('settings/', views.settings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('hot/', views.hot, name='hot_questions')
]
