from django.contrib import admin
from .models import DocumentTemplate


@admin.register(DocumentTemplate)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'file',
        'class_level',
        'uploaded_at',
    )
    list_display_links = ('name', 'class_level')
