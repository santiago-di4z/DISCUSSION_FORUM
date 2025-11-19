from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import reg_form

# Registration View
def reg_view(request):
    if request.method == 'POST':
        form = reg_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        
    else:
        form = reg_form()

    return render(request, 'users/register.html',  {'form': form})

# Login View
def lin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

# Logout View
def lout_view(request):
    logout(request)
    return redirect('home')
