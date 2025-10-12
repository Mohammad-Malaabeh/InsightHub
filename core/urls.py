from django.urls import path
from . import views


urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_update, name='project_update'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),

    # Manager/Admin Reports
    path('manager/reports/', views.manager_reports, name='manager_reports'),
    path('manage-users/', views.manage_users, name='manage_users'),

    # Tasks
    path('projects/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', views.task_update, name='task_update'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    
]
