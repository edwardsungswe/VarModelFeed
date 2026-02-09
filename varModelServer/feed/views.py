import mimetypes
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from rest_framework import generics, pagination, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from .models import Post
from .serializers import MediaUploadSerializer, PostCreateSerializer, PostSerializer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostListView(generics.ListAPIView):
    queryset = Post.objects.select_related("author").order_by("created_at")
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        author = User.objects.get(pk=serializer.validated_data.pop("author_id"))
        serializer.save(author=author)


class MediaUploadView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = MediaUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        content_type = uploaded_file.content_type or ""

        if content_type.startswith("image/"):
            media_folder = "images"
            max_size_bytes = 5 * 1024 * 1024
            kind = "image"
        elif content_type.startswith("video/"):
            media_folder = "videos"
            max_size_bytes = 50 * 1024 * 1024
            kind = "video"
        else:
            return Response(
                {"detail": "Only image and video uploads are supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded_file.size > max_size_bytes:
            return Response(
                {"detail": f"{kind.capitalize()} file exceeds size limit."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        upload_dir = os.path.join(settings.MEDIA_ROOT, media_folder)
        os.makedirs(upload_dir, exist_ok=True)

        extension = os.path.splitext(uploaded_file.name)[1].lower()
        safe_name = f"{uuid.uuid4().hex}{extension}"
        storage = FileSystemStorage(location=upload_dir)
        saved_name = storage.save(safe_name, uploaded_file)

        url = request.build_absolute_uri(f"/api/media/{media_folder}/{saved_name}/")
        return Response({"url": url, "media_type": kind}, status=status.HTTP_201_CREATED)


class MediaFileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, media_folder, filename):
        if media_folder not in {"images", "videos"}:
            raise Http404("Invalid media folder.")

        file_path = os.path.join(settings.MEDIA_ROOT, media_folder, filename)
        if not os.path.isfile(file_path):
            raise Http404("File not found.")

        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        return FileResponse(open(file_path, "rb"), content_type=content_type)
