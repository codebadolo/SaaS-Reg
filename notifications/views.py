from django.shortcuts import render
from accounts.models import Agency, Agent
from .models import Notification
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Create your views here.
def notification_list(request):
    print("provider_list view is being called!")
    return HttpResponse("Provider List View")  # Replace with your actual view logic@login_required

@login_required
def notification_list(request):
    agency = None
    try:
        agency = Agency.objects.get(owner=request.user)
    except Agency.DoesNotExist:
        pass

    if agency:
        notifications = Notification.objects.filter(agency=agency).order_by('-timestamp')
    else:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    return render(request, 'accounts/notification_list.html', {
        'notifications': notifications,
        'agency': agency  # Pass the agency object to the template
    })

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')