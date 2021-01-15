from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),

    # questions
    path('questions/', views.question_list, name="question_list"),
    path('questions/<int:pk>', views.question_detail, name="question_detail"),
    path('questions/<int:pk>/vote', views.vote, name="vote"),
    path('search/', views.search, name="search"),

    #topic
    path('topics/', views.topic_list, name="topic_list"),
    path('topics/<int:pk>', views.topic_detail, name="topic_detail"),

]
