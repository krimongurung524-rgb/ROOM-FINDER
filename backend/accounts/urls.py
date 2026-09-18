from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('password/change/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/saved-rooms/', views.saved_rooms_view, name='saved_rooms'),
    path('dashboard/inquiries/', views.inquiries_view, name='inquiries'),
    path('dashboard/visits/', views.visits_view, name='visits'),
    path('dashboard/messages/', views.messages_view, name='messages'),
]