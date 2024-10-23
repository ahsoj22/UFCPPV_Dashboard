
from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro_view, name='intro'),      
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    path('update_fight_info/', views.update_fight_info, name='update_fight_info'),
    path('trend_analysis/', views.trend_analysis, name='trend_analysis'),
]
