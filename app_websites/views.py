from django.shortcuts import render
from .models import *

def home(request):
    context = { 
            'orders' : Order.objects.all(),
            }
    return render(request, 'app_websites/home.html', context )
