from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Property(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('shared', 'Shared Room'),
        ('1bhk', '1BHK Flat'),
        ('2bhk', '2BHK Apartment'),
        ('flat', 'Flat'),
        ('house', 'House'),
    ]

    CITY_CHOICES = [
        ('dharan', 'Dharan'),
        ('itahari', 'Itahari'),
        ('kathmandu', 'Kathmandu'),
        ('pokhara', 'Pokhara'),
        ('biratnagar', 'Biratnagar'),
        ('birtamod', 'Birtamod'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        help_text='Property owner (must belong to accounts app User model)',
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)

    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    area = models.CharField(max_length=100, help_text='e.g. Bhanuchowk, Putali Line')
    address = models.CharField(max_length=255, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    monthly_rent = models.PositiveIntegerField()
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)

    # Facilities
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_attached_bathroom = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    is_furnished = models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:details', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f'Image for {self.property.title}'
