from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Post, Tag, User
from .forms import SignUpForm, ProjectForm, TaskForm, PostForm, LoginForm

# --- dashboard view ---
def dashboard(request):
    context = {
        'project_count': Project.objects.count(),
        'task_count': Task.objects.count(),
        'post_count': Post.objects.count(),
        'all_projects': Project.objects.count(),
        'all_users': User.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)


# --- manager and admin views ---
def manager_reports(request):
    projects = Project.objects.prefetch_related('tasks').all()
    tasks = Task.objects.select_related('project').all()
    return render(request, 'core/manager_reports.html', {'projects': projects, 'tasks': tasks})

def manage_users(request):
    users = User.objects.all()
    return render(request, 'core/manage_users.html', {'users': users})


# --- Project Views ---
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)

            default_owner = User.objects.first()
            project.owner = default_owner
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form})

def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form})

def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('project_list')