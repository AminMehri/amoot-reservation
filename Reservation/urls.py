from django.urls import path
from Reservation import views

urlpatterns = [
    path("departments", views.GetDepartments.as_view(), name="depatments"),
    path("single-department", views.GetSingleDepatment.as_view(), name="single-department"),
    path("doctors", views.GetDoctors.as_view(), name="doctors"),
    path("single-doctor", views.GetSingleDoctor.as_view(), name="single-doctor"),
    path("update-doctor-info", views.UpdateDoctorInfo.as_view(), name="update-doctor-info"),
    path("patient-info", views.GetPatientInfo.as_view(), name="patient-info"),
    path("update-patient-info", views.UpdatePatientInfo.as_view(), name="update-patient-info"),
    path("time-slots", views.GetTimeSlot.as_view(), name="time-slots"),
    path("add-free-time", views.DoctorAddFreeTime.as_view(), name="add-free-time"),
    path("remove-free-time", views.DoctorRemoveFreeTime.as_view(), name="remove-free-time"),
    path("free-times", views.GetDoctorFreeTime.as_view(), name="free-times"),
    path("add-reservation", views.AddReservation.as_view(), name="add-reservation"),
    path("remove-reservation", views.RemoveReservation.as_view(), name="remove-reservation"),
    path("create-timeslot", views.CreateTimeSlot.as_view(), name='create-timeslot'),
]
