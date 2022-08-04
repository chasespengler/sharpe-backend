from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, ClientForm
from .models import *

def dashboard(request):
    cur_client = request.user.client
    ports = cur_client.portfolio_set.all()
    context = {'client': cur_client, 'portfolios': ports}
    return render(request, 'sharpe_analysis/dashboard.html', context)

def registration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(
                user=user, 
                first_name = user.first_name, 
                last_name=user.last_name, 
                email=user.email
                )
            messages.success(request, 'Account successfully created!')
            return redirect('login')
    context = {'register_form':form}
    return render(request, 'sharpe_analysis/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'sharpe_analysis/login.html', context)
