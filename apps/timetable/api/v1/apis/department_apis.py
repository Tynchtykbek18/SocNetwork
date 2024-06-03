from rest_framework import generics

from apps.timetable.api.v1.serializers import DepartmentSerializer
from apps.timetable.models import Department


class DepartmentListAPI(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailAPI(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentCreateAPI(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentUpdateAPI(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDeleteAPI(generics.DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
