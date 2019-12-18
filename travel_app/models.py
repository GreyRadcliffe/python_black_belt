from django.db import models
import bcrypt
from datetime import date

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be atleast 3 characters."
        if len(postData['username']) < 3:
            errors['username'] = "Username must be atleast 3 characters."
        if len(User.objects.filter(username= postData['username'])) > 0:
            errors['username_taken'] = "That username is already taken."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters."
        if not postData['confirm_password'] == postData['password']:
            errors['password_match'] = "Passwords do not match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        filterUsername = User.objects.filter(username= postData['username'])
        if len(filterUsername) < 1:
            errors['username'] = "That username or password does not exist."
        elif not bcrypt.checkpw(postData['password'].encode(), filterUsername[0].password.encode()):
            errors['password'] = "The password you entered does not match the email."
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        today = str(date.today())
        if len(postData['destination']) < 1 or len(postData['description']) < 1 or not postData['travel_from'] or not postData['travel_to']:
            errors['destination'] = "No field may be left empty."
        if postData['travel_from'] < today:
            errors['date_from'] = "Date of trip must happen in the future."
        if postData['travel_to'] < postData['travel_from']:
            errors['date_to'] = "The trip must end after it begins."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_from = models.DateField()
    travel_to = models.DateField()
    objects = TripManager()
    creator = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name= "trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





