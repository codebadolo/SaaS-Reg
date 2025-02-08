from django.shortcuts import render

# Create your views here.
# transactions/views.py
def transaction_register(request):
    print("transaction_register view is being called!")
    return HttpResponse("Transaction Register View")  # Replace with your actual view logic
