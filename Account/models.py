from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass



class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email_verify_token = models.CharField(max_length=256, null=True)
    email_verify_generate_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    email_verified = models.BooleanField(default=False)
    reset_token_created_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    reset_password_token = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.user.username
