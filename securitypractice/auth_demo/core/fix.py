from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('core.can_view_reports')  # format: 'app_label.codename'
def view_reports(request):
    return render(request, 'core/reports.html')
