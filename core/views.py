from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Post, Tag, User
from .forms import ProjectForm, TaskForm, PostForm

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

# --- Task Views ---
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'core/task_list.html', {'project': project, 'tasks': tasks})

def all_tasks(request):
    projects = Project.objects.all().prefetch_related('tasks')
    return render(request, 'core/all_tasks.html', {'projects': projects})

def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form, 'project': project})

def task_update(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'project': project})

def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)
    task.delete()
    return redirect('task_list', project_id=project_id)

# --- Post Views ---
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            default_owner = User.objects.first()
            post.owner = default_owner
            post.save()

            tags_text = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_text.split(',') if t.strip()]
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag_obj)

            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form})

def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_form.html', {'form': form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    u = User.objects.first()
    if u:
        if u in post.liked_by.all():
            post.liked_by.remove(u)
        else:
            post.liked_by.add(u)
    return redirect('post_list')