# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import User
from django.contrib import messages

# Create your views here.
def logout(request):
    request.session.flush()
    return redirect('/')

def index(request):
    return render(request,'login_app/index.html')

def register(request):
    results = User.objects.registerVal(request.POST)
    if results['status'] == False:
        User.objects.createUser(request.POST)
        messages.success(request, "User has been created")
    else:
        for error in results['errors']:
            messages.error(request, error)

    return redirect('/')

def login(request):
    results = User.objects.loginVal(request.POST)
    if results['status'] == True:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['name'] = results['user'].name
        request.session['id'] = results['user'].id
        request.session['email'] = results['user'].email
        return redirect('friends/dashboard')


