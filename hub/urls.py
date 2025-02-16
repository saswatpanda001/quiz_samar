from django.contrib import admin
from django.urls import path,include
from hub.views import quiz, leaderboard, rules, login, get_quiz_data, levels, profile_edit, profile_view, quiz1, dashboard, landing, update_quiz_data, level_completed, quiz_completed, quiz_details, profile_view_others

app_name = "hub"

urlpatterns = [
    path('',landing,name="landing"),
    path('dashboard',dashboard,name="dashboard"),
    
    path('quiz/<str:quiz_idd>/<int:level>/<int:ques>', quiz,name="quiz"),
    path('quiz/<str:quiz_idd>/', quiz_details,name="quiz_details"),
    
    path('level/<str:quiz_idd>/<int:level>/', level_completed,name="level_comp"),
    path('quiz/<str:quiz_idd>/<int:level>/complete', quiz_completed,name="quiz_comp"),
    
    path('leaderboard', leaderboard,name="leaderboard"),
    path('rules', rules,name="rules"),
    path('levels',levels,name="levels"),
    path('quiz/update',update_quiz_data,name="update_quiz"),

    path('profile/', profile_view, name='profile_view'),
    path('profile/<int:id>', profile_view_others, name='profile_view_others'),
    path('profile/edit/', profile_edit, name='profile_edit'),


    path("get_quiz_data/level/<int:level>/", get_quiz_data, name="get_quiz_data"),

    #path('quiz1', quiz1,name="quiz1"),
    #path('login',login,name="login"),

]

