from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Reservation, Doctor
from django.db.models import F


@receiver(post_delete, sender=Reservation)
def increase_doctor_capacity(sender, instance, **kwargs):
    # Increase the doctor's capacity by 1 when a reservation is deleted
    instance.doctor.capacity = F('capacity') + 1
    instance.doctor.save()
