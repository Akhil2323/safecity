from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Authority(models.Model):

    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    AUTH_USER=models.OneToOneField(User,on_delete=models.CASCADE)

class Bus(models.Model):
    bus_name=models.CharField(max_length=100)
    reg_no=models.CharField(max_length=100)
    ownername=models.CharField(max_length=100)
    owneremail=models.CharField(max_length=100)

class Route(models.Model):
    from_destination=models.CharField(max_length=100)
    to_destination=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longititude=models.CharField(max_length=100)

class Stop(models.Model):
    ROUTE=models.ForeignKey(Route,on_delete=models.CASCADE)
    stopname=models.CharField(max_length=100)

class Assign_route(models.Model):
    BUS=models.ForeignKey(Bus,on_delete=models.CASCADE)
    ROUTE=models.ForeignKey(Route,on_delete=models.CASCADE)

class usersprofile(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    Auth_USER=models.OneToOneField(User,on_delete=models.CASCADE)


class Place(models.Model):
    stop=models.ForeignKey(Stop,on_delete=models.CASCADE)
    placename=models.CharField(max_length=1000)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    placetype=models.CharField(max_length=1001)


class Alert(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=100,default='danger')
    time=models.TimeField()
    date=models.DateField()
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)



class Complaint(models.Model):
    complaint = models.TextField()
    reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, default='pending')
    date = models.CharField(max_length=100)
    USER = models.ForeignKey(usersprofile, on_delete=models.CASCADE)

