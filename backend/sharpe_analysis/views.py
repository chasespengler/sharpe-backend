from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, PortModalForm
from django.contrib.auth.decorators import login_required
from .models import *
from .data_get import *
from .calculations import *
import asyncio

@login_required(login_url='login')
def dashboard(request):
    cur_client = request.user.client
    ports = cur_client.portfolio_set.all()
    AddPortForm = inlineformset_factory(Client, Portfolio, fields=('portfolio_name',), extra=1)
    form = AddPortForm(queryset=Portfolio.objects.none(), instance=cur_client)
    context = {'client': cur_client, 'portfolios': ports, 'form':form}
    if request.method == 'POST':
        form = AddPortForm(request.POST, instance=cur_client)
        if form.is_valid():
            z = []
            for x in ports.values('portfolio_name'):
                z.append(x['portfolio_name'])
            if form.cleaned_data[0].get('portfolio_name') not in z:
                form.save()
            else:
                messages.info(request, 'Portfolio with that name already exists.')
    return render(request, 'sharpe_analysis/dashboard.html', context)

@login_required(login_url='login')
#Will need security to manage wether a person has access to the portfolio or not
def portfolioPage(request, pid):
    cur_client = request.user.client
    portfolio = cur_client.portfolio_set.get(id=pid)
    context = {'client':cur_client, 'portfolio':portfolio}
    return render(request, 'sharpe_analysis/portfolio_page.html', context)

@login_required(login_url='login')
def editPort(request, pid):
    EditPortForm = inlineformset_factory(Portfolio, Security, fields=('ticker', 'security_type', 'amount'), extra=1)
    port = Portfolio.objects.get(id=pid)
    secs = port.security_set.all()
    form = EditPortForm(queryset=Security.objects.none(), instance=port)
    if request.method == "POST":
        form = EditPortForm(request.POST, instance=port)
        if form.is_valid():
            tick = form.cleaned_data[0].get('ticker')
            ticks = secs.values('ticker')
            for x in ticks:
                if x['ticker'] == tick:
                    messages.info(request, "You've already added this ticker.")
                    context = {'port':port, 'formy':form, 'secs': secs}
                    return render(request, 'sharpe_analysis/edit_portfolio.html', context)
            form.save()
            form = EditPortForm(queryset=Security.objects.none(), instance=port)
            
    context = {'port':port, 'formy':form, 'secs': secs}
    return render(request, 'sharpe_analysis/edit_portfolio.html', context)

@login_required(login_url='login')
def del_port(request, pid):
    Portfolio.objects.filter(id=pid).delete()
    return redirect('dashboard')

@login_required(login_url='login')
def del_sec(request, sid, pid):
    Security.objects.filter(id=sid).delete()
    return editPort(request, pid)

@login_required(login_url='login')
def analyze(request, pid):
    port = Portfolio.objects.get(id=pid)
    secs = port.security_set.all()
    tickers = []
    for sec in secs:
        tickers.append(sec.ticker)
    bad, good = needs_adding(tickers)
    if bad:
        add_eq_data(bad)
        data = get_eq_data(tickers)
    else:
        data = get_eq_data(tickers)
    print(data)
    print(secs.values())
    port.sharpe = calc_sharpe(data, secs.values())
    port.save()

    print(port.sharpe)

    return redirect('dashboard')

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

def logoutUser(request):
    logout(request)
    return redirect('login')
