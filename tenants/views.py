from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Tenant
from .forms import TenantForm, ContactManagerForm
from notifications.models import Notification

@login_required
@role_required(['owner', 'manager'])
def tenant_list(request):
    if request.user.role == 'owner':
        tenants = Tenant.objects.filter(property__owner=request.user)
    else:
        tenants = Tenant.objects.filter(property__manager=request.user)
    return render(request, 'tenants/tenant_list.html', {'tenants': tenants})

@login_required
@role_required(['owner', 'manager'])
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            tenant = form.save(commit=False)
            if tenant.unit:
                tenant.property = tenant.unit.property
                # Mark unit as occupied
                tenant.unit.is_occupied = True
                tenant.unit.save()
            tenant.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'tenants/tenant_form.html', {'form': form, 'title': 'Add Tenant'})

@login_required
@role_required(['tenant'])
def pay_rent(request):
    try:
        tenant = request.user.tenant_profile
        if not tenant.property:
            messages.warning(request, "You are not assigned to any property yet.")
            return redirect('dashboard')
            
        return render(request, 'tenants/pay_rent.html', {'tenant': tenant})
    except Tenant.DoesNotExist:
        messages.error(request, "Tenant profile not found.")
        return redirect('dashboard')

@login_required
@role_required(['tenant'])
def contact_manager(request):
    try:
        tenant = request.user.tenant_profile
        if not tenant.property:
            messages.warning(request, "You are not assigned to any property yet.")
            return redirect('dashboard')
            
        # Determine recipient (Manager or Owner)
        recipient = tenant.property.manager if tenant.property.manager else tenant.property.owner
        
        if request.method == 'POST':
            form = ContactManagerForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message_body = form.cleaned_data['message']
                
                # Create notification for the manager/owner
                full_message = f"Message from {request.user.first_name} {request.user.last_name} (Unit {tenant.unit.unit_number if tenant.unit else 'N/A'}): {subject}\n\n{message_body}"
                Notification.objects.create(
                    user=recipient,
                    message=full_message,
                    link="#" # Could link to tenant detail or a message view if we had one
                )
                
                messages.success(request, f"Message sent to {recipient.first_name} {recipient.last_name}.")
                return redirect('dashboard')
        else:
            form = ContactManagerForm()
            
        return render(request, 'tenants/contact_manager.html', {
            'form': form, 
            'recipient': recipient,
            'tenant': tenant
        })
        
    except Tenant.DoesNotExist:
        messages.error(request, "Tenant profile not found.")
        return redirect('dashboard')
