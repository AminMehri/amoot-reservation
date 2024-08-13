from django.test import TestCase, Client
from django.urls import reverse
from Reservation.models import Reservation, Doctor, Department, Patient
from django.shortcuts import get_object_or_404
from Account.models import Account, User


class GetTicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get-ticket') 
    
    def test_get_ticket_success(self):
        Department.objects.create(name='Dentistry', slug='test', description='test', id=1)
        dep = get_object_or_404(Department, id=1)
        Doctor.objects.create(full_name='test' ,department=dep ,slug='test' ,description='test' ,capacity=20 ,phone='test' ,office_address='test', id=1)
        doc = get_object_or_404(Doctor, id=1)
        User.objects.create_user(username='testuser', password='testpass123', email='test.test@test.test')
        user = get_object_or_404(User, username='testuser')
        Account.objects.create(user=user, id=1)
        acc = get_object_or_404(Account, id=1)
        Patient.objects.create(account=acc, full_name='test', gender='m', phone='test', address='test')

        response = self.client.post(self.url, {
            'patient_id': 1,
            'doctor_id': 1,
        })
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json().get("message"), "Reservation created successfully")
    
    def test_get_ticket_invalid_p_id(self):
        response = self.client.post(self.url, {
            'patient_id': "a",
            'doctor_id': 1,
        })
        
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json().get("message"), "invalid data")
    
    def test_get_ticket_exist_ticket(self):
        Department.objects.create(name='Dentistry', slug='test', description='test', id=1)
        dep = get_object_or_404(Department, id=1)
        Doctor.objects.create(full_name='test' ,department=dep ,slug='test' ,description='test' ,capacity=20 ,phone='test' ,office_address='test', id=1)
        doc = get_object_or_404(Doctor, id=1)
        User.objects.create_user(username='testuser', password='testpass123', email='test.test@test.test')
        user = get_object_or_404(User, username='testuser')
        Account.objects.create(user=user, id=1)
        acc = get_object_or_404(Account, id=1)
        Patient.objects.create(account=acc, full_name='test', gender='m', phone='test', address='test', id=1)
        pat = get_object_or_404(Patient, id=1)

        Reservation.objects.create(doctor=doc, patient=pat)
        response = self.client.post(self.url, {
            'patient_id': 1,
            'doctor_id': 1,
        })
        
        self.assertEqual(response.status_code, 208)

        self.assertEqual(response.json().get("message"), "reservation is alreay exist")
