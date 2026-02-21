from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Property, Unit
from .forms import PropertyForm, UnitForm
from accounts.models import User

@login_required
@role_required(['owner', 'manager'])
def property_list(request):
    if request.user.role == 'owner':
        properties = Property.objects.filter(owner=request.user)
    else:
        properties = Property.objects.filter(manager=request.user)
    return render(request, 'properties/property_list.html', {'properties': properties})

@login_required
@role_required(['owner'])
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form, 'title': 'Add Property'})

@login_required
@role_required(['owner', 'manager'])
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    # Check permissions
    if request.user.role == 'owner' and property_obj.owner != request.user:
        return redirect('dashboard')
    if request.user.role == 'manager' and property_obj.manager != request.user:
        return redirect('dashboard')
        
    units = property_obj.units.all()
    return render(request, 'properties/property_detail.html', {'property': property_obj, 'units': units})

@login_required
@role_required(['owner'])
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj, user=request.user)

    return render(request, 'properties/property_form.html', {
        'form': form,
        'title': 'Edit Property'
    })


@login_required
@role_required(['owner', 'manager'])
def add_unit(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    # Permission check
    if request.user.role == 'owner' and property_obj.owner != request.user:
        return redirect('dashboard')
    if request.user.role == 'manager' and property_obj.manager != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.property = property_obj
            unit.save()
            return redirect('property_detail', pk=property_id)
    else:
        form = UnitForm()
    return render(request, 'properties/unit_form.html', {'form': form, 'property': property_obj})
