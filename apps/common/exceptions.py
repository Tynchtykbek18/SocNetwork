from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class ExceptionHandlerMixin:
    def handle_exception(self, exc):
        logger.error(f"Error in view {self.__class__.__name__}: {str(exc)}", exc_info=True)
        return Response({"error": "A server error occurred. Please try again later."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
