from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TENANT = 'tenant'
    OWNER = 'owner'
    USER_TYPE_CHOICES = [
        (TENANT, 'Tenant'),
        (OWNER, 'Property Owner'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=TENANT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_owner(self):
        return self.user_type == self.OWNER

    @property
    def is_tenant(self):
        return self.user_type == self.TENANT