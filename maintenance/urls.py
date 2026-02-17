from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_request, name='maintenance_new'),
    path('<int:pk>/', views.request_detail, name='maintenance_detail'),
    path('<int:pk>/update/', views.update_request_status, name='update_request_status'),
]
