from django.urls import path

from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('map/', views.map_view, name='map'),
    path('map/data/', views.map_data, name='map_data'),
    path('add/', views.add_property, name='add_property'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('<slug:slug>/', views.details, name='details'),
    path('<slug:slug>/edit/', views.edit_property, name='edit_property'),
    path('<slug:slug>/delete/', views.delete_property, name='delete_property'),
]
