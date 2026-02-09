from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'created_at']
    search_fields = ['title', 'company_name']
    list_filter = ['created_at']
    readonly_fields = ['id', 'created_at']
