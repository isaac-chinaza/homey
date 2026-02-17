from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm



@login_required
def request_detail(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    # Security check: only allow tenant (creator), owner, or manager of the property
    is_authorized = False
    if request.user == req.tenant:
        is_authorized = True
    elif request.user.role == 'owner' and req.property.owner == request.user:
        is_authorized = True
    elif request.user.role == 'manager' and req.property.manager == request.user:
        is_authorized = True
        
    if not is_authorized:
        return redirect('dashboard')

    return render(request, 'maintenance/detail.html', {'request_obj': req})

def create_request(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/create.html', {'form': form})


def update_request_status(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MaintenanceRequestForm(instance=req)
    return render(request, 'maintenance/update.html', {'form': form})
