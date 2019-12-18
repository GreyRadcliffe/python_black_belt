from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt, re

def main(request):
    return render(request, "main.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name = request.POST['name']
        username = request.POST['username']
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(name= name, username= username, password= pwhash)
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(username= request.POST['username']).id
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    context = {
        "logged_user" : User.objects.get(id= request.session['user_id']),
        "other_users" : User.objects.exclude(id= request.session['user_id']),
        "all_trips" : Trip.objects.all(),
        "joined_trips" : Trip.objects.filter(users=User.objects.get(id=request.session['user_id']))
    }
    return render(request, 'travels.html', context)

def addTrip(request):
    if request.method == "POST":
        print(request.POST)
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/travels/add')
        else:
            creator = User.objects.get(id= request.session['user_id'])
            Trip.objects.create(destination= request.POST['destination'], description= request.POST['description'], creator= creator,travel_from= request.POST['travel_from'], travel_to= request.POST['travel_to'])
            return redirect('/travels')
    return render(request, "addTrip.html")

def showTrip(request, x):
    context = {
        "trip" : Trip.objects.get(id=x)
    }
    return render(request, "showTrip.html", context)

def joinTrip(request, x):
    Trip.objects.get(id=x).users.add(User.objects.get(id=request.session['user_id']))
    return redirect("/travels")