from django.urls import path
from .views import MediaFileView, MediaUploadView, PostCreateView, PostListView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('media/upload/', MediaUploadView.as_view(), name='media-upload'),
    path('media/<str:media_folder>/<str:filename>/', MediaFileView.as_view(), name='media-file'),
]
