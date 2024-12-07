from django.contrib import admin
from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'status', 'created_at')
    search_fields = ('tracking_number', 'user__username')
    list_filter = ('status','user')
    fields = ('tracking_number', 'user', 'status', 'pickup_code')
    ordering = ('-created_at',)  # řazení sestupně

