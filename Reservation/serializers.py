from rest_framework import serializers



class ReservationSerializer(serializers.Serializer):
    username = serializers.CharField()
    id = serializers.CharField()



class PatientInfoSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    age = serializers.IntegerField()



class DoctorInfoSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    department = serializers.CharField()
    phone = serializers.CharField()
    office_address = serializers.CharField()
    description = serializers.CharField()
    content = serializers.CharField()
    thumbnail = serializers.CharField()