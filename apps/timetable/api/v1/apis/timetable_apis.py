from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response

from apps.timetable.api.v1.serializers import (
    CourseSerializer,
    DepartmentSerializer,
    LessonSerializer,
)
from apps.timetable.models import Course, Department


class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TimeTableList(views.APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "department_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID кафедра"),
                "course_number": openapi.Schema(type=openapi.TYPE_INTEGER, description="Номер курса"),
            },
        )
    )
    def post(self, request):
        department_id = request.data.get("department_id")
        course_number = request.data.get("course_number")

        if not department_id or not course_number:
            return Response(
                {"error": "Department ID and course number are required in the query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            department = Department.objects.get(pk=department_id)
            course = Course.objects.prefetch_related("lessons").get(department=department, course=course_number)
            lessons = course.lessons.all()
        except Department.DoesNotExist:
            return Response({"error": "Department matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "Course matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "department": DepartmentSerializer(department).data,
            "course": CourseSerializer(course).data,
            "lessons": LessonSerializer(lessons, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)
