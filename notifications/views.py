from django.shortcuts import render

# Create your views here.
def notification_list(request):
    print("provider_list view is being called!")
    return HttpResponse("Provider List View")  # Replace with your actual view logic