# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login_app.models import User

# Create your views here.

def dashboard(request):
	currentUser = User.objects.get(id= request.session['id'])
	others = User.objects.exclude(id=request.session['id'])
	# User.objects.exclude(friended=currentUser)
	context = {
	    # 'myFriends': User.objects.exclude(get(id= request.session['id']).friends.all()),
	    'friends': currentUser.friends.all(),
	    'other_users': others.exclude(friended=currentUser)
	}
	return render(request, 'second_app/dashboard.html', context)

def profile(request, id):
	context = {
	    'user': User.objects.get(id = id),
	    'other_users': User.objects.exclude(id = request.session['id'])
	}
	return render(request, 'second_app/profile.html', context)

def addFriend(request, id):
    User.objects.get(id = request.session['id']).friends.add(User.objects.get(id = id))
    return redirect('/friends/dashboard')

def edit(request, id):
    context = {
	    'user': User.objects.get(id = id),
	    'other_users': User.objects.exclude(id = request.session['id'])
    }
    return render(request, "second_app/edit.html", context)

def update(request, id):
    user = User.objects.get(id = id)
    user.name = request.POST['name']
    user.alias = request.POST['alias']
    user.email = request.POST['email']
    
    request.session['name'] = user.name
    request.session['alias'] = user.alias
    request.session['email'] = user.email
    user.save()

    return render(request,'second_app/dashboard.html')


def delete(request, id):
    theUnfriendedFriend = User.objects.get(id = id)
    user = User.objects.get(id = request.session['id'])
    user.friends.remove(theUnfriendedFriend)
    return redirect('/friends/dashboard')