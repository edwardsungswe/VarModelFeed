from rest_framework import serializers
from .models import Post
from user.models import User


class AuthorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "company_name",
            "logo_placeholder",
            "title",
            "description",
            "detailed_description",
            "images",
            "videos",
            "created_at",
        ]

    def get_author(self, obj):
        if obj.author is None:
            return None
        return {"id": obj.author.id, "name": obj.author.name}


class PostCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Post
        fields = [
            "author_id",
            "company_name",
            "logo_placeholder",
            "title",
            "description",
            "detailed_description",
            "images",
            "videos",
        ]

    def validate_author_id(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return value

    def validate_images(self, value):
        return value or []

    def validate_videos(self, value):
        return value or []


class MediaUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
