from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------------
# Custom User Model
# -------------------------------
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('Admin', 'Admin'),
            ('Manager', 'Manager'),
            ('Staff', 'Staff'),
        ],
        default='Staff'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.is_superuser = bool(self.is_superuser)
        self.is_staff = bool(self.is_staff)

        if self.is_superuser:
            if self.role != 'Admin':
                self.role = 'Admin'
            self.is_staff = True
        else:
            if self.role == 'Admin':
                self.is_superuser = True
                self.is_staff = True
            else:
                pass

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username


# -------------------------------
# Project Model
# -------------------------------
class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------------
# Task Model
# -------------------------------
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# -------------------------------
# Tag Model
# -------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -------------------------------
# Post Model
# -------------------------------
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title