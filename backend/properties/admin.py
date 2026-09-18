from django.contrib import admin

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'city', 'area', 'room_type',
        'monthly_rent', 'is_available', 'created_at',
    )
    list_filter = ('city', 'room_type', 'is_available', 'has_wifi', 'has_parking', 'is_furnished')
    search_fields = ('title', 'area', 'address')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]
