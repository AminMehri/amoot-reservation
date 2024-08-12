from django.db import models
from ckeditor.fields import RichTextField
from Account.models import Account
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator



class Department(models.Model):
    DEP_CHOICES = (
        ('Dentistry', 'Dentistry'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Cardiology', 'Cardiology'),
        ('Emergency', 'Emergency'),
        ('Forensic Pathology', 'Forensic Pathology'),
    )
    name = models.CharField(max_length=256, choices=DEP_CHOICES, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    description = RichTextField()

    def __str__(self):
        return self.name



class Doctor(models.Model):
    full_name = models.CharField(max_length=256)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=128, unique=True)
    description = RichTextField()
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
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.full_name



class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'doctor'], name='unique_patient_doctor')
        ]

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
