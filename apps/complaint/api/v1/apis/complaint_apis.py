from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.complaint.api.v1.serializers.complaint_serializers import (
    ComplaintSerializer,
    PostWithComplaintsSerializer,
)
from apps.post.models.post_models import Post


class ComplaintCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ComplaintSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostsWithComplaintsListView(generics.ListAPIView):
    serializer_class = PostWithComplaintsSerializer

    def get_queryset(self):
        # Получаем все посты и сортируем их по количеству жалоб в убывающем порядке
        queryset = (
            Post.objects.annotate(complaints_count=Count("complaints"))
            .filter(complaints_count__gt=0)
            .order_by("-complaints_count")
        )
        return queryset
