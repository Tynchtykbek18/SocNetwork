from django.contrib import admin

from apps.complaint.models.complaint_models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "reason", "created_at")
    list_display_links = ("id", "post", "reason", "created_at")
