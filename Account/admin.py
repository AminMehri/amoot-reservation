from django.contrib import admin
from Account import models

admin.site.register(models.User)
admin.site.register(models.Account)