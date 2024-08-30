from rest_framework.permissions import BasePermission, SAFE_METHODS
from Reservation.models import Patient, Doctor


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        self.message = 'شما به عنوان یک بیمار ثبت نشده اید.'
        if not Patient.objects.filter(account__user=request.user).exists():
            return False
        return bool(request.user)



class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        self.message = 'شما به عنوان یک بیمار ثبت نشده اید.'
        if not Doctor.objects.filter(account__user=request.user).exists():
            return False
        return bool(request.user)