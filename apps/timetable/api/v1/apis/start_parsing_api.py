from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, views

from apps.timetable.parser import parsing


class StartParsingAPI(views.APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "start": openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number page"),
                "end": openapi.Schema(type=openapi.TYPE_INTEGER, description="End number page"),
            },
        )
    )
    def post(self, request):
        parsing(start=int(request.data["start"]), end=int(request.data["end"]))
        return response.Response({"status": "ok"})
