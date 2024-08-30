from django.contrib import admin
from Reservation import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('account', 'full_name', 'department', 'capacity', 'phone', 'office_address')
    search_fields = ['full_name', 'department', 'capacity', 'phone', 'office_address']


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('account', 'full_name', 'gender', 'phone', 'age')
    search_fields = ['account', 'full_name', 'phone', 'age']


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'reserved_date')
    search_fields = ['doctor', 'patient', 'reserved_date']


@admin.register(models.AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor','reserved_date_func')
    search_fields = ['doctor']

    def reserved_date_func(self, obj):
        return " ,".join([str(p.date) + ' : ' + p.time_range for p in obj.free_date.all()])
    reserved_date_func.short_description = "Free Time"


@admin.register(models.TimeSlot)
class TimeSlot(admin.ModelAdmin):
    list_display = ('date','time_range')
    search_fields = ['date','time_range']