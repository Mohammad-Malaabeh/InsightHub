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
