from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, manager_or_admin_required
from .models import Project, Task, Post, Tag, User
from .forms import ProjectForm, TaskForm, PostForm, SignUpForm, LoginForm, ProfileForm
from django.contrib import messages

#--- Authentication imports ---
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


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
@manager_or_admin_required
def manager_reports(request):
    projects = Project.objects.prefetch_related('tasks').all()
    tasks = Task.objects.select_related('project').all()
    return render(request, 'core/manager_reports.html', {'projects': projects, 'tasks': tasks})

@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'core/manage_users.html', {'users': users})


@admin_required
@require_POST
def toggle_user_role(request, user_id):
    target = get_object_or_404(User, id=user_id)
    # Do not allow modifying Admins
    if target.role == 'Admin':
        messages.error(request, "Cannot change role of an Admin.")
        return redirect('manage_users')
    # Toggle Manager <-> Staff
    target.role = 'Staff' if target.role == 'Manager' else 'Manager'
    # Persist flags coherently with your User.save() logic
    # Non-admin roles should not be superuser; keep staff flag as appropriate
    target.is_superuser = False
    target.is_staff = (target.role == 'Manager')
    target.save()
    messages.success(request, f"Updated {target.username}'s role to {target.role}.")
    return redirect('manage_users')

@admin_required
@require_POST
def delete_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target.role == 'Admin':
        messages.error(request, "Cannot delete an Admin.")
        return redirect('manage_users')
    if target.id == request.user.id:
        messages.error(request, "You cannot delete your own account.")
        return redirect('manage_users')
    target.delete()
    messages.success(request, "User deleted.")
    return redirect('manage_users')



# --- Project Views ---
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})

@manager_or_admin_required
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

@manager_or_admin_required
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

@manager_or_admin_required
@require_http_methods(["GET", "POST"])
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        return redirect('project_list')

    return render(request, 'core/project_confirm_delete.html', {'project': project})

# --- Task Views ---
@login_required
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'core/task_list.html', {'project': project, 'tasks': tasks})

@login_required
def all_tasks(request):
    projects = Project.objects.all().prefetch_related('tasks')
    return render(request, 'core/all_tasks.html', {'projects': projects})

@manager_or_admin_required
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

@manager_or_admin_required
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

@manager_or_admin_required
def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)
    task.delete()
    return redirect('task_list', project_id=project_id)

# --- Post Views ---
@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/post_list.html', {'posts': posts})

@login_required
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

@login_required
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

@login_required
@require_http_methods(["GET", "POST"])
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'core/post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    u = request.user
    if u in post.liked_by.all():
        post.liked_by.remove(u)
    else:
        post.liked_by.add(u)
    return redirect('post_list')

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    context = {
        "form": form,
        "role": user.role,
        "date_joined": getattr(user, "date_joined", None),
        "created_at": getattr(user, "created_at", None),
    }
    return render(request, "core/profile.html", context)