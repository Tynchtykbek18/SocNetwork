from rest_framework import generics

from apps.timetable.api.v1.serializers import CourseSerializer
from apps.timetable.models import Course


class CourseListAPI(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailAPI(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreateAPI(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateAPI(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDeleteAPI(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
