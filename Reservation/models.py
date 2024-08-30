from django.db import models
from ckeditor.fields import RichTextField
from Account.models import Account
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator
from Utils.models import BaseReservation


class Department(BaseReservation):
    DEP_CHOICES = (
        ('Dentistry', 'Dentistry'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Cardiology', 'Cardiology'),
        ('Emergency', 'Emergency'),
        ('Forensic Pathology', 'Forensic Pathology'),
    )
    name = models.CharField(max_length=256, choices=DEP_CHOICES, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    thumbnail =  models.ImageField(upload_to='media/departments')

    def __str__(self):
        return self.name



class Doctor(BaseReservation):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='media/doctors')
    capacity = models.IntegerField(validators=[MaxValueValidator(30), MinValueValidator(0)])
    phone = models.CharField(max_length=13)
    office_address = models.CharField(max_length=1024)

    def __str__(self):
        return self.full_name



class Patient(models.Model):
    GEN_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('n', 'Non binary')
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=1, choices=GEN_CHOICES)
    age = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    phone = models.CharField(max_length=13)
    
    def __str__(self):
        return self.full_name
    


class TimeSlot(models.Model):
    TIME_SLOT = (
        ('8-10', '8-10'),
        ('10-12', '10-12'),
        ('12-14', '12-14'),
        ('14-16', '14-16'),
        ('16-18', '16-18'),
        ('18-20', '18-20'),
    )
    date = models.DateField()
    time_range = models.CharField(max_length=5, choices=TIME_SLOT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'time_range'], name='unique_date_time')
        ]
    
    def __str__(self):
        return f'{self.date} - {self.time_range}'



class AppointmentSlot(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, unique=True)
    free_date = models.ManyToManyField(TimeSlot, blank=True)

    def __str__(self):
        return f'{self.doctor.full_name} - {self.free_date}'
    


class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reserved_date = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.doctor.capacity > 0:
                self.doctor.capacity = F('capacity') - 1
                self.doctor.save()
            else:
                raise ValueError("Doctor capacity is full!")
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.doctor.full_name + ' <--- ' + self.patient.full_name
