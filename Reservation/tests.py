from django.test import TestCase, Client
from django.urls import reverse
from Reservation.models import Reservation, Doctor, Department, Patient
from Account.models import Account, User



class GetTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get-ticket') 

        self.department = Department.objects.create(name='Dentistry', slug='test', description='test', id=1)
        self.doctor = Doctor.objects.create(full_name='test' ,department=self.department ,slug='test' ,description='test' ,capacity=20 ,phone='test' ,office_address='test', id=1)
        self.doctor2 = Doctor.objects.create(full_name='test2' ,department=self.department ,slug='test2' ,description='test2' ,capacity=20 ,phone='test2' ,office_address='test2', id=2)
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='test.test@test.test')
        self.account = Account.objects.create(user=self.user, id=1)
        self.patient = Patient.objects.create(account=self.account, full_name='test', gender='m', phone='test', address='test')
        self.reservation = Reservation.objects.create(doctor=self.doctor2, patient=self.patient)

    # def test_get_ticket_success(self):

    #     response = self.client.post(self.url, {
    #         'patient_id': 1,
    #         'doctor_id': 1,
    #     }, content_type="application/json")
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json().get("message"), "Reservation created successfully")
    
    # def test_get_ticket_invalid_p_id(self):

    #     response = self.client.post(self.url, {
    #         'patient_id': "a",
    #         'doctor_id': 1,
    #     }, content_type="application/json")
        
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json().get("message"), "invalid data")
    
    # def test_get_ticket_exist_ticket(self):

    #     response = self.client.post(self.url, {
    #         'patient_id': 1,
    #         'doctor_id': 2,
    #     }, content_type="application/json")
        
    #     self.assertEqual(response.status_code, 208)
    #     self.assertEqual(response.json().get("message"), "reservation is alreay exist")
    
    # def test_get_ticket_int_id(self):

    #     response = self.client.post(self.url, {
    #         'patient_id': "1",
    #         'doctor_id': 1
    #     }, content_type="application/json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json().get("message"), "patient id must be an integer")



class ReservationModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name='Dentistry', slug='test', description='test', id=1)
        self.doctor = Doctor.objects.create(full_name='test' ,department=self.department ,slug='test' ,description='test' ,capacity=20 ,phone='test' ,office_address='test', id=1)
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='test.test@test.test')
        self.account = Account.objects.create(user=self.user, id=1)
        self.patient = Patient.objects.create(account=self.account, full_name='test', gender='m', phone='test', address='test')
        self.reservation = Reservation.objects.create(doctor=self.doctor, patient=self.patient,)

    def test_reservation_decreases_capacity(self):
        
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.capacity, 19)

    def test_reservation_delete_decreases_capacity(self):

        self.reservation.delete()
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.capacity, 20)