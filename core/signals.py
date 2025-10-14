from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Task, Post

def push_to_user(user_id, payload):
    try:
        layer = get_channel_layer()
        if not layer:
            return
        async_to_sync(layer.group_send)(f"user_{user_id}", {"type": "notify", "payload": payload})
    except Exception:
        pass

def notify_admin_by_email(subject, message):
    recipients = getattr(settings, "ADMIN_ALERT_EMAILS", None) or [getattr(settings, "DEFAULT_FROM_EMAIL", None)]
    recipients = [r for r in recipients if r]
    if recipients:
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        except Exception:
            pass

# Project
@receiver(post_save, sender=Project)
def project_created_or_updated(sender, instance, created, **kwargs):
    payload = {"kind": "project", "event": "created" if created else "updated", "project_id": instance.id, "name": instance.name}
    push_to_user(instance.owner_id, payload)
    notify_admin_by_email(
        f"[InsightHub] Project {'created' if created else 'updated'}: {instance.name}",
        f"Project: {instance.name}\nOwner: {instance.owner.username} ({instance.owner.email})\n",
    )

@receiver(post_delete, sender=Project)
def project_deleted(sender, instance, **kwargs):
    if instance.owner_id:
        push_to_user(instance.owner_id, {"kind": "project", "event": "deleted", "project_id": instance.id, "name": instance.name})
    notify_admin_by_email(f"[InsightHub] Project deleted: {instance.name}", f"Project: {instance.name}\n")

# Task
@receiver(post_save, sender=Task)
def task_created_or_updated(sender, instance, created, **kwargs):
    payload = {
        "kind": "task", "event": "created" if created else "updated",
        "task_id": instance.id, "title": instance.title, "completed": instance.completed,
        "project_id": instance.project_id, "project_name": instance.project.name,
    }
    push_to_user(instance.project.owner_id, payload)
    if getattr(instance, 'assignee_id', None):
        push_to_user(instance.assignee_id, payload)
    notify_admin_by_email(
        f"[InsightHub] Task {'created' if created else 'updated'}: {instance.title}",
        f"Project: {instance.project.name}\nTask: {instance.title}\nCompleted: {instance.completed}\nOwner: {instance.project.owner.username} ({instance.project.owner.email})\n",
    )

@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    owner_id = getattr(instance.project, "owner_id", None) if getattr(instance, "project", None) else None
    if owner_id:
        push_to_user(owner_id, {"kind": "task", "event": "deleted", "task_id": instance.id, "title": instance.title, "project_id": getattr(instance, "project_id", None)})
    if getattr(instance, 'assignee_id', None):
        push_to_user(instance.assignee_id, {"kind": "task", "event": "deleted", "task_id": instance.id, "title": instance.title})
    notify_admin_by_email(f"[InsightHub] Task deleted: {instance.title}", f"Task: {instance.title}\nProject ID: {getattr(instance, 'project_id', None)}\n")

# Post
@receiver(post_save, sender=Post)
def post_created_or_updated(sender, instance, created, **kwargs):
    push_to_user(instance.owner_id, {"kind": "post", "event": "created" if created else "updated", "post_id": instance.id, "title": instance.title})
    notify_admin_by_email(f"[InsightHub] Post {'created' if created else 'updated'}: {instance.title}", f"Author: {instance.owner.username}\nTitle: {instance.title}\n")

@receiver(post_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    if instance.owner_id:
        push_to_user(instance.owner_id, {"kind": "post", "event": "deleted", "post_id": instance.id, "title": instance.title})
    notify_admin_by_email(f"[InsightHub] Post deleted: {instance.title}", f"Title: {instance.title}\n")