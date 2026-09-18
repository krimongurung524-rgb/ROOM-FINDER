from django import forms
from django.forms import inlineformset_factory

from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'room_type', 'city', 'area', 'address',
            'latitude', 'longitude', 'monthly_rent', 'bedrooms', 'bathrooms',
            'has_wifi', 'has_parking', 'has_attached_bathroom', 'has_kitchen',
            'is_furnished', 'is_available',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the property...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Single Room near Bhanuchowk'}),
            'area': forms.TextInput(attrs={'placeholder': 'e.g. Bhanuchowk'}),
            'address': forms.TextInput(attrs={'placeholder': 'Full address'}),
            'monthly_rent': forms.NumberInput(attrs={'placeholder': 'Rs.'}),
            'latitude': forms.NumberInput(attrs={'placeholder': 'e.g. 26.812500', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'placeholder': 'e.g. 87.283300', 'step': 'any'}),
        }


PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    fields=['image', 'is_primary'],
    extra=3,
    can_delete=True,
)


class PropertySearchForm(forms.Form):
    ROOM_TYPE_CHOICES = [('', 'All Room Types')] + Property.ROOM_TYPE_CHOICES
    CITY_CHOICES = [('', 'All Locations')] + Property.CITY_CHOICES

    q = forms.CharField(required=False, label='Search')
    city = forms.ChoiceField(required=False, choices=CITY_CHOICES)
    area = forms.CharField(required=False)
    room_type = forms.ChoiceField(required=False, choices=ROOM_TYPE_CHOICES)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    wifi = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    furnished = forms.BooleanField(required=False)
