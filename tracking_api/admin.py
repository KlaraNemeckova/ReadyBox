from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'user', 'status', 'created_at')  # zobrazení ve výpisu
    search_fields = ('tracking_number', 'user__username')  # hledání podle tracking_number a username
    list_filter = ('status', 'user')  # filtr podle status a user

    # Použití metody get_status_display() pro správné zobrazení statusu
    def get_status_display(self, obj):
        return obj.get_status_display()  # Django se postará o human-friendly formát

    fields = ('tracking_number', 'user', 'status', 'pickup_code')  # políčka pro záznam v administraci
    ordering = ('-created_at',)  # řazení podle created_at sestupně
