from django.urls import path
from Reservation import views

urlpatterns = [
    path("get-ticket", views.GetTicket.as_view(), name="get-ticket")
]
