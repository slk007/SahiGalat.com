from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .forms import UserCreationForm, UserLoginForm

User = get_user_model()

def signupuser(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            username_ = form.cleaned_data.get('username')
            user_obj = User.objects.get(username__iexact=username_)
            login(request, user_obj)
            
            return redirect('question_list')
        else:
            return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'Wrong Inputs'})    
    else:
        return render(request, 'signupuser.html', {'form': UserCreationForm()})

def loginuser(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            
            username_ = form.cleaned_data.get('username')
            user_obj = User.objects.get(username__iexact=username_)

            login(request, user_obj)
            return redirect('question_list')
        else:
            return render(request, 'loginuser.html', {'form': UserLoginForm(), 'error': 'Invalid Credentials !!'})
    else:
        return render(request, 'loginuser.html', {'form': UserLoginForm()})

@login_required
def signoutuser(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')