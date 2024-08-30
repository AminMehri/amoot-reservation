from rest_framework.views import APIView
from Reservation.models import Department, Doctor, Patient, Reservation as Reservation_model, TimeSlot, AppointmentSlot
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Reservation import serializers
from Account.models import Account
from Reservation.permissions import IsDoctor, IsPatient



class GetDepartments(APIView):
    def post(self, request):
        departments = Department.objects.all().order_by('name')
        data = []
        for dep in departments:
            data.append({
                "name": dep.name,
                "slug": dep.slug,
                "image": dep.thumbnail.url,
                "description": dep.description
            })
        return Response(data, status=status.HTTP_200_OK)



class GetSingleDepatment(APIView):
    def post(self, request):
        slug = request.data.get("slug")
        department = get_object_or_404(Department, slug=slug)
        department_data = [{
            "name": department.name,
            "slug": department.slug,
            "content": department.content
        }]

        # Doctor's who work in this department
        doctors = Doctor.objects.filter(department=department)
        doctor_data = []
        for doc in doctors:
            doctor_data.append({
                "full_name": doc.full_name,
                "username": doc.account.user.username,
                "description": doc.description,
                "thumbnail": doc.thumbnail.url
            })
        return Response({"doctor_data": doctor_data, "department_data": department_data}, status=status.HTTP_200_OK)



class GetDoctors(APIView):
    def post(self, request):
        doctors = Doctor.objects.all().order_by('full_name')
        data = []
        for doc in doctors:
            data.append({
                "full_name": doc.full_name,
                "username": doc.account.user.username,
                "description": doc.description,
                "department": doc.department.name,
                "department_slug": doc.department.slug,
                "thumbnail": doc.thumbnail.url
            })
        return Response(data, status=status.HTTP_200_OK)



class GetSingleDoctor(APIView):
    def post(self, request):
        username = request.data.get("username")
        account = get_object_or_404(Account, user__username=username)
        doctor = get_object_or_404(Doctor, account=account)
        docor_data = [{
            "full_name": doctor.full_name,
            "username": doctor.account.user.username,
            "content": doctor.content,
            "department": doctor.department.name,
            "department_slug": doctor.department.slug,
            "phone": doctor.phone,
            "office_address": doctor.office_address
        }]

        # Doctor's who work in the same department with this doctor
        related_doctors = Doctor.objects.filter(department=doctor.department).exclude(id=doctor.id)
        related_doctors_data = []
        for doc in related_doctors:
            related_doctors_data.append({
                "full_name": doc.full_name,
                "username": doc.account.user.username,
                "description": doc.description,
                "thumbnail": doc.thumbnail.url
            })
        return Response({"docor_data": docor_data, "related_doctors_data": related_doctors_data}, status=status.HTTP_200_OK)



class UpdateDoctorInfo(APIView):
    permission_classes = [IsAuthenticated&IsDoctor]

    def post(self, request):
        try:
            username = request.data.get("username")
            # for updating the doctor information the doctor must be the same user who is logged in
            if request.user.username != username:
                return Response({"message": "You are not allowed to update this doctor information"}, status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.DoctorInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "invalid data", "detail": f"invalid date for: {' ,'.join(serializer.errors)}"}, status=status.HTTP_400_BAD_REQUEST)
            
            Doctor.objects.filter(account__user__username=username).update(
                full_name=serializer.data.get("full_name"),
                department=serializer.data.get("department"),
                phone=serializer.data.get("phone"),
                office_address=serializer.data.get("office_address"),
                description=serializer.data.get("description"),
                content=serializer.data.get("content"),
                thumbnail=serializer.data.get("thumbnail")
            )
            return Response({"message": "Your information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetPatientInfo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        account = get_object_or_404(Account, user__username=username)
        # for seeing the patient information the patient must be the same user who is logged in
        # or the patient must be the doctor's patient
        if username == request.user.username or Reservation_model.objects.filter(
            doctor__account__user=request.user, patient__account__user__username=username
        ).exists():
            patient = get_object_or_404(Patient, account=account)
            data = [{
                "full_name": patient.full_name,
                "username": patient.account.user.username,
                "gender": patient.gender,
                "phone": patient.phone
            }]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not allowed to see this patient information"}, status=status.HTTP_403_FORBIDDEN)



class UpdatePatientInfo(APIView):
    permission_classes = [IsAuthenticated&IsPatient]

    def post(self, request):
        try:
            # for updating the patient information the patient must be the same user who is logged in
            username = request.data.get("username")
            if request.user.username != username:
                return Response({"message": "You are not allowed to update this patient information"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = serializers.PatientInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "invalid data", "detail": f"invalid date for: {' ,'.join(serializer.errors)}"}, status=status.HTTP_400_BAD_REQUEST)

            Patient.objects.filter(account__user__username=username).update(
                full_name=serializer.data.get("full_name"),
                gender=serializer.data.get("gender"),
                age=serializer.data.get("age"),
                phone=serializer.data.get("phone"),
            )
            return Response({"message": "Patient information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Show for doctors
class GetTimeSlot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        time_slots = TimeSlot.objects.all()
        data = []
        for t in time_slots:
            data.append({
                'id': t.id,
                'date': t.date,
                'time_range': t.time_range,
            })
        return Response(data, status=status.HTTP_200_OK)



# Dotor's schedules their free times
class DoctorAddFreeTime(APIView):
    permission_classes = [IsAuthenticated&IsDoctor]

    def post(self, request):
        try:
            user = request.user
            # a few time ids. example: 2 3 4
            time_ids = request.data.get("id").split(" ")

            doctor = get_object_or_404(Doctor, account__user=user)

            if AppointmentSlot.objects.filter(doctor=doctor).exists():
                app_slot = AppointmentSlot.objects.get(doctor=doctor)
            else:
                app_slot = AppointmentSlot.objects.create(doctor=doctor)
            
            errors = []
            for time in time_ids:
                try:
                    app_slot.free_date.add(TimeSlot.objects.get(id=time))
                except Exception as e:
                    errors.append(str(e))
            
            if len(errors) > 0:
                return Response({"message": "Something went wrong for some time slots", "detail": errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Appointment slots created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Something went wrong", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Dotor's schedules their free times
class DoctorRemoveFreeTime(APIView):
    permission_classes = [IsAuthenticated&IsDoctor]

    def post(self, request):
        try:
            user = request.user
            # list of time ids
            time_ids = request.data.get("id").split(" ")

            doctor = get_object_or_404(Doctor, account__user=user)

            if AppointmentSlot.objects.filter(doctor=doctor).exists():
                app_slot = AppointmentSlot.objects.get(doctor=doctor)
            else:
                return Response({"message": "Appointment slots does not created", "detail": "Please create appoinment slot"}, status=status.HTTP_400_BAD_REQUEST)
            
            errors = []
            for time in time_ids:
                try:
                    app_slot.free_date.remove(TimeSlot.objects.get(id=time))
                except Exception as e:
                    errors.append(str(e))
            
            if len(errors) > 0:
                return Response({"message": "Something went wrong for some time slots", "detail": errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Appointment slots removed successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Something went wrong", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Show for patient
class GetDoctorFreeTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # doctor username
        username = request.data.get("username")
        doctor = get_object_or_404(Doctor, account__user__username=username)

        doctor_appslots = AppointmentSlot.objects.filter(doctor=doctor)
        data = []
        for slot in doctor_appslots:
            data.append({
                "slot_id": slot.id,
                "free_times": [{"date": a.date, "time_range": a.time_range, "id": a.id} for a in slot.free_date.all()]
            })
        return Response(data, status=status.HTTP_200_OK)



class AddReservation(APIView):
    permission_classes = [IsAuthenticated&IsPatient]

    def post(self, request):
        serializer = serializers.ReservationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "invalid data", "detail": f"invalid date for: {' ,'.join(serializer.errors)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Time slot id
        id = serializer.data.get("id")
        # Doctor username
        username = serializer.data.get("username")
        doctor = get_object_or_404(Doctor, account__user__username=username)

        patient = get_object_or_404(Patient, account__user=request.user)

        app_doctor = AppointmentSlot.objects.get(doctor=doctor)
        if not app_doctor.free_date.filter(id=id).exists():
            return Response({"message": "Doctor is not free at this time.", "detail": "Please choose another time"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Reservation_model.objects.filter(doctor=doctor, reserved_date__id=id):
            return Response({"message": "This time is reserved already", "detail": "Please choose another time"}, status=status.HTTP_400_BAD_REQUEST)
        
        time_slot = TimeSlot.objects.get(id=id)

        Reservation_model.objects.create(doctor=doctor, reserved_date=time_slot, patient=patient)
        app_doctor.free_date.remove(time_slot)
        return Response({"message": "Reservation is created successfully"}, status=status.HTTP_201_CREATED)



class RemoveReservation(APIView):
    permission_classes = [IsAuthenticated&IsPatient]

    def post(self, request):
        # Reservation id
        id = request.data.get("id")
        
        if not Reservation_model.objects.filter(id=id, patient__account__user=request.user).exists():
            return Response({"message": "There is not such a reservation"}, status=status.HTTP_400_BAD_REQUEST)
        
        reservation = get_object_or_404(Reservation_model, id=id)
        app_doctor = AppointmentSlot.objects.get(doctor=reservation.doctor)
        app_doctor.free_date.add(reservation.reserved_date)
        Reservation_model.objects.filter(id=id).delete()
        return Response({"message": "Reservation is deleted successfully"}, status=status.HTTP_200_OK)



class CreateTimeSlot(APIView):
    def post(self, request):
        slots = ['8-10','10-12','12-14','14-16','16-18','18-20']
        for s in slots:
            TimeSlot.objects.create(date='2024-05-24', time_range=s)

        return Response(status=status.HTTP_200_OK)