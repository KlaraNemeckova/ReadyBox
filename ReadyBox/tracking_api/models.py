from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    STATUS_CHOICES = [
        ('in_box', 'In box'),
        ('ready_for_pickup', 'Ready for pickup'),
        ('picked_up', 'Picked up'),
    ]

    tracking_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_box')
    pickup_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"

class PackageHistory(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.package.tracking_number} - {self.status} at {self.changed_at}"
