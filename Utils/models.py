from django.db import models
from ckeditor.fields import RichTextField



class BaseReservation(models.Model):
    description = models.TextField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True