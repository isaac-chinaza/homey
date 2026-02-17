from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from properties.models import Property
from maintenance.models import MaintenanceRequest
from tenants.models import Tenant

@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'owner':
        properties = Property.objects.filter(owner=user)
        total_properties = properties.count()
        active_tenants = Tenant.objects.filter(property__in=properties, is_active=True).count()
        pending_maintenance = MaintenanceRequest.objects.filter(property__in=properties, status='pending').count()
        
        context.update({
            'properties': properties,
            'total_properties': total_properties,
            'active_tenants': active_tenants,
            'pending_maintenance': pending_maintenance,
            'dashboard_type': 'owner'
        })
    elif user.role == 'manager':
        properties = Property.objects.filter(manager=user)
        maintenance_requests = MaintenanceRequest.objects.filter(property__in=properties, status='pending')
        context.update({
            'properties': properties,
            'maintenance_requests': maintenance_requests,
            'dashboard_type': 'manager'
        })
    elif user.role == 'tenant':
        try:
            tenant = user.tenant_profile
            maintenance_requests = MaintenanceRequest.objects.filter(tenant=user)
            context.update({
                'tenant': tenant,
                'maintenance_requests': maintenance_requests,
                'dashboard_type': 'tenant'
            })
        except Tenant.DoesNotExist:
            context['error'] = "Tenant profile not found."
    elif user.role == 'admin':
         context['dashboard_type'] = 'admin'

    return render(request, 'dashboard/dashboard.html', context)
