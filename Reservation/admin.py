from django.contrib import admin
from Reservation import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'slug', 'capacity', 'phone', 'office_address')
    search_fields = ['full_name', 'department', 'slug', 'capacity', 'phone', 'office_address']
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('account', 'full_name', 'gender', 'phone', 'address')
    search_fields = ['account', 'full_name', 'phone', 'address']


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient')
    search_fields = ['doctor', 'patient']
