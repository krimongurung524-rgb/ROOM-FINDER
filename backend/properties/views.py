from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PropertyForm, PropertyImageFormSet, PropertySearchForm
from .models import Property


def home(request):
    """Landing page - shows a handful of featured/popular properties."""
    featured = Property.objects.filter(is_available=True)[:8]
    return render(request, 'home/home.html', {'featured_properties': featured})


def search(request):
    """Browse + filter page. Supports normal page load and AJAX (live) search."""
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(is_available=True)

    if form.is_valid():
        data = form.cleaned_data
        if data.get('q'):
            properties = properties.filter(
                Q(title__icontains=data['q']) | Q(area__icontains=data['q'])
            )
        if data.get('city'):
            properties = properties.filter(city=data['city'])
        if data.get('area'):
            properties = properties.filter(area__icontains=data['area'])
        if data.get('room_type'):
            properties = properties.filter(room_type=data['room_type'])
        if data.get('min_price'):
            properties = properties.filter(monthly_rent__gte=data['min_price'])
        if data.get('max_price'):
            properties = properties.filter(monthly_rent__lte=data['max_price'])
        if data.get('wifi'):
            properties = properties.filter(has_wifi=True)
        if data.get('parking'):
            properties = properties.filter(has_parking=True)
        if data.get('furnished'):
            properties = properties.filter(is_furnished=True)

    paginator = Paginator(properties, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render(
            request, 'components/room_card_list.html', {'page_obj': page_obj}
        ).content.decode('utf-8')
        return JsonResponse({'html': html, 'count': paginator.count})

    return render(request, 'properties/search.html', {
        'form': form,
        'page_obj': page_obj,
        'total': paginator.count,
    })


def map_view(request):
    """Renders the map page shell; actual markers are loaded via map_data (AJAX)."""
    return render(request, 'properties/map.html')


def map_data(request):
    """JSON endpoint consumed by static/js/map.js to plot markers."""
    properties = Property.objects.filter(
        is_available=True, latitude__isnull=False, longitude__isnull=False
    )
    data = [{
        'id': p.id,
        'title': p.title,
        'lat': float(p.latitude),
        'lng': float(p.longitude),
        'rent': p.monthly_rent,
        'url': p.get_absolute_url(),
    } for p in properties]
    return JsonResponse({'properties': data})


def details(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    return render(request, 'properties/details.html', {'property': property_obj})


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
            if formset.is_valid():
                formset.save()
            messages.success(request, 'Property published successfully!')
            return redirect('properties:my_properties')
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet()
    return render(request, 'properties/add_property.html', {'form': form, 'formset': formset})


@login_required
def edit_property(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_obj)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('properties:my_properties')
    else:
        form = PropertyForm(instance=property_obj)
        formset = PropertyImageFormSet(instance=property_obj)
    return render(request, 'properties/edit_property.html', {
        'form': form,
        'formset': formset,
        'property': property_obj,
    })


@login_required
def delete_property(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted.')
        return redirect('properties:my_properties')
    return render(request, 'properties/confirm_delete.html', {'property': property_obj})


@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/my_properties.html', {'properties': properties})
