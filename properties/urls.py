from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/update/', views.property_update, name='property_update'),
    path('<int:property_id>/add-unit/', views.add_unit, name='add_unit'),
]
