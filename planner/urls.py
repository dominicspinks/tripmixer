from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.planner_dashboard, name='planner-dashboard'),
    path('holidays/', views.holidays_list, name='holiday-list'),
    path('holidays/add', views.HolidayCreate.as_view(), name='holiday-create'),
    path('holidays/<int:pk>/update/', views.HolidayUpdate.as_view(), name='holiday-update'),
    path('holidays/<int:pk>/delete/', views.HolidayDelete.as_view(), name='holiday-delete'),
    path('holidays/<int:pk>/', views.holidays_detail, name='holiday-detail'),
    path('holidays/<int:holiday_id>/destinations/add/',views.destination_create,name='destination-create'),
    path('holidays/<int:holiday_id>/destinations/<int:pk>/delete/', views.DestinationDelete.as_view(), name='destination-delete'),
    path('holidays/<int:holiday_id>/destinations/<int:pk>/update/', views.DestinationUpdate.as_view(), name='destination-update'),
    path('holidays/<int:holiday_id>/destinations/<int:destination_id>/', views.destinations_detail, name='destination-detail'),
    path('destinations/<int:destination_id>/itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary-detail'),
    path('destinations/<int:destination_id>/itinerary/add', views.ItinCreate.as_view(), name='itinerary-create'),
    path('destinations/<int:destination_id>/itinerary/<int:pk>/update', views.ItinUpdate.as_view(), name='itinerary-update'),
    path('destinations/<int:destination_id>/itinerary/<int:pk>/delete', views.ItinDelete.as_view(), name='itinerary-delete'),
    path('destinations/<int:destination_id>/itinerary/<int:itinerary_id>/accommodation', views.AccomCreate.as_view(), name='accom-create'),
    path('destinations/<int:destination_id>/itinerary/<int:itinerary_id>/accommodation/<int:accommodation_id>/update', views.AccomUpdate.as_view(), name='accom-update'),
    path('destinations/<int:destination_id>/itinerary/<int:itinerary_id>/accommodation/delete', views.AccomDelete.as_view(), name='accom-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
