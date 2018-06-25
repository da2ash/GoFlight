from .forms import SignUp
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

def login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user_id = user.id
                auth_login(request, user)
                return redirect('/users/demo_login/')
        else:
            return render(request, 'users/login.html', {'user': user})
    return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':
        user_form = SignUp(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            auth_login(request, authenticate(username=username, password=password))
            return redirect('/users/demo_login/')
    else:
        user_form = SignUp()
    return render(request, 'users/register.html', {'user_form': user_form})


@login_required(login_url='/users/login/')
def demo_login(request):
    return render(request, 'users/demo_login.html')
