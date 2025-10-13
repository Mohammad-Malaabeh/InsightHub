from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'Admin')(view_func)

def manager_or_admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role in ['Admin', 'Manager'])(view_func)
