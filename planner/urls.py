from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.planner_dashboard, name='planner-dashboard'),
    path('holidays/', views.holidays_list, name='holiday-list'),
    path('holidays/new', views.HolidayCreate.as_view(), name='holiday-create'),
    path('holidays/<int:pk>/', views.holidays_detail, name='holiday-detail'),
    path('holidays/<int:holiday_id>/add_destination/',views.add_destination,name='add_destination'),
    path('holidays/<int:holiday_id>/destinations/<int:pk>/delete/', views.destination_delete.as_view(), name='destination-delete'),
    path('holidays/<int:holiday_id>/destinations/<int:pk>/update/', views.destination_update.as_view(), name='destination-update'),
    path('holidays/<int:holiday_id>/destinations/<int:destination_id>/', views.destinations_detail, name='destinations-detail'),
    path('destinations/<int:destination_id>/itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary-detail'),
    path('destinations/<int:destination_id>/itinerary/create', views.ItinCreate.as_view(), name='itinerary_create'),
    path('destinations/<int:destination_id>/itinerary/<int:pk>/update', views.ItinUpdate.as_view(), name='itinerary_update'),
    path('destinations/<int:destination_id>/itinerary/<int:pk>/delete', views.ItinDelete.as_view(), name='itinerary_delete'),
    path('accounts/signup/', views.signup, name='signup'),

]
