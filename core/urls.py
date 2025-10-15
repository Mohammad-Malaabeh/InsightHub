from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


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
    path('manage-users/<int:user_id>/toggle-role/', views.toggle_user_role, name='toggle_user_role'),
    path('manage-users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    # Tasks
    path('projects/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', views.task_update, name='task_update'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),

    # Posts
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_update, name='post_update'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
]
