from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'loginreg/index.html')

def register(request):
    errors = User.objects.registation_validator(request.POST)
    if (type(errors) == User):
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password']),
        request.session['user_id'] = errors.id
    else:
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if (type(errors)==User):
        request.session['user_id'] = errors.id
        return redirect('/success')
    else:
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    context = {'user': User.objects.get(id=request.session['user_id'])}
    return render(request, 'loginreg/success.html', context)

def logout(request):
    del request.session['user_id']
    return redirect('/')