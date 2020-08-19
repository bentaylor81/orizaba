from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .decorators import unauthenticated_user

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try: 
            user = authenticate(request, username=User.objects.get(email=username), password=password)
        except:
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/orders')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')