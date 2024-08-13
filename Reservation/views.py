from rest_framework.views import APIView
from Reservation.models import Department, Doctor, Patient, Reservation
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Reservation.serializers import GetTicketSerializer



class GetTicket(APIView):

    def post(self, request):

        serializer = GetTicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "invalid data", "detail": f"invalid date for: {' ,'.join(serializer.errors)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        patient_id = request.data.get("patient_id")
        if not isinstance(patient_id, int):
            return Response({"message": "patient id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        doctor_id = int(serializer.data.get('doctor_id'))
        patient_id = int(serializer.data.get('patient_id'))

        doc = get_object_or_404(Doctor, id=doctor_id)
        pat = get_object_or_404(Patient, id=patient_id)
        
        if Reservation.objects.filter(doctor=doctor_id, patient=patient_id).exists():
            return Response({"message": "reservation is alreay exist"}, status=status.HTTP_208_ALREADY_REPORTED)
        
        try:
            Reservation.objects.create(doctor=doc, patient=pat)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Reservation created successfully"}, status=status.HTTP_200_OK)
