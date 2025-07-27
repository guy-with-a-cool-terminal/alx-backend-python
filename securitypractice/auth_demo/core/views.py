from django.shortcuts import render
from django.contrib.auth.decorators import login_required,permission_required

@login_required
def dashboard(request):
    return render(request,'core/dashboard.html')

@permission_required('core.can_view_reports')
def view_reports(request):
    return render(request,'core/reports.html')