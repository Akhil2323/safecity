import json
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt

import pickle
import pandas as pd
from django.http import JsonResponse
from .utils import predict_risk

from myapp.models import *


# Create your views here.
def home(request):
    return render(request,'home.html')


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    user=authenticate(request,username=uname, password=pwd)

    if user is not None:

        if user.groups.filter(name='admin').exists():

            login(request,user)

            return redirect('/myapp/adminhome/')

        else:
            messages.error(request, "user profile is not founded")
            return redirect('/myapp/login_get/')

    else:

        messages.error(request, "Invalid username or password")
        return redirect('/myapp/login_get/')

def logout_view(request):
    logout(request)
    return redirect('/myapp/login_get/')

    # ====================================================================================================
# admin module
@login_required(login_url='/myapp/login_get/')
def adminindex(request):
    return render(request,'adminindex.html')

@login_required(login_url='/myapp/login_get/')
def addauthority_get(request):
    return render(request,'addauthority.html')

@login_required(login_url='/myapp/login_get/')
def addauthority_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    city = request.POST['city']
    district = request.POST['district']
    pin = request.POST['pin']

    # Generate random password
    pwd = random.randint(10000, 99999)

    if User.objects.filter(username=email).exists():
        return render(request,'addauthority.html',{'message':'email already exists'})

    # Create user
    u = User.objects.create_user(
        username=email,
        password=str(pwd),
        email=email
    )
    u.groups.add(Group.objects.get(name='authority'))
    u.save()

    # Save authority details
    Authority.objects.create(
        AUTH_USER=u,
        name=name,
        email=email,
        phone=phone,
        place=place,
        city=city,
        district=district,
        pin=pin,
    )

    # Email sending
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("leagaladvisorteam@gmail.com", "eugnxtyylwtqwlav")

    message = f"""Subject: Authority Login Credentials

Dear {name},

You are registered as an Authority.

Username: {email}
Password: {pwd}

Regards,
Legal Advisor Team
"""

    server.sendmail(
        'legaladvisorteam@gmail.com',
        email,
        message
    )
    server.quit()

    return redirect('/myapp/viewauthority/')


@login_required(login_url='/myapp/login_get/')
def viewauthority(request):
    data=Authority.objects.all()
    return render(request,'viewauthority.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editauthority_get(request,id):
    data=Authority.objects.get(id=id)
    return render(request,'editauthority.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editauthority_post(request):
    id = request.POST['id']

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    city = request.POST['city']
    district = request.POST['district']
    pin = request.POST['pin']

    # Check if email exists for another authority (exclude current one)
    email_exists = Authority.objects.filter(email=email).exclude(id=id).exists()

    if email_exists:
        messages.error(request, "Email already exists!")
        return redirect(f'/myapp/editauthority_get/{id}')

    # Update authority
    i = Authority.objects.get(id=id)
    i.name = name
    i.email = email
    i.phone = phone
    i.place = place
    i.city = city
    i.district = district
    i.pin = pin
    i.save()

    messages.success(request, "Authority updated successfully")
    return redirect('/myapp/viewauthority/')

@login_required(login_url='/myapp/login_get/')
def deleteauthority(request,id):
    data=Authority.objects.get(id=id)
    data.delete()
    return redirect('/myapp/viewauthority/')

@login_required(login_url='/myapp/login_get/')
def addbus_get(request):
    return render(request,'addbus.html')

@login_required(login_url='/myapp/login_get/')
def addbus_post(request):
    bname = request.POST['busname']
    regno = request.POST['regno']
    ownnam = request.POST['ownername']
    ownem = request.POST['owneremail']

    # Check if bus name + reg no already exists
    bus_exists = Bus.objects.filter(
        reg_no=regno
    ).exists()

    if bus_exists:
        print("Bus already exists")
        messages.error(request, "register number already exist")
        return redirect('/myapp/addbus_get/')   # back to add page

    # Save new bus
    i = Bus()
    i.bus_name = bname
    i.reg_no = regno
    i.ownername = ownnam
    i.owneremail = ownem
    i.save()

    messages.success(request, "Bus added successfully")
    return redirect('/myapp/viewbus/')

@login_required(login_url='/myapp/login_get/')
def viewbus(request):
    data=Bus.objects.all()

    return render(request,'viewbus.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editbus_get(request,id):
    data=Bus.objects.get(id=id)
    return render(request,'editbus.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editbus_post(request):
    id = request.POST['id']
    bname = request.POST['busname']
    regno = request.POST['regno']
    ownnam = request.POST['ownername']
    ownem = request.POST['owneremail']

    # Check if register number exists for another bus
    reg_exists = Bus.objects.filter(reg_no=regno).exclude(id=id).exists()

    if reg_exists:
        print("Register number already exists")
        messages.error(request, "Register number already exists")
        return redirect(f'/myapp/editbus_get/{id}')

    i = Bus.objects.get(id=id)
    i.bus_name = bname
    i.reg_no = regno
    i.ownername = ownnam
    i.owneremail = ownem
    i.save()

    messages.success(request, "Bus updated successfully")
    return redirect('/myapp/viewbus/')

@login_required(login_url='/myapp/login_get/')
def deletebus(request,id):
    data=Bus.objects.get(id=id)
    data.delete()
    return redirect('/myapp/viewbus/')

@login_required(login_url='/myapp/login_get/')
def addroute_get(request):
    return render(request,'addroute.html')

@login_required(login_url='/myapp/login_get/')
def addroute_post(request):
    fd=request.POST['from_destination']
    td=request.POST['to_destination']
    lt=request.POST['latitude']
    lg=request.POST['longititude']
    i=Route()
    i.from_destination=fd
    i.to_destination=td
    i.latitude=lt
    i.longititude=lg
    i.save()
    return redirect('/myapp/viewroute/')

@login_required(login_url='/myapp/login_get/')
def viewroute(request):
    data=Route.objects.all()
    return render(request,'viewroute.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editroute_get(request,id):
    data=Route.objects.get(id=id)
    return render(request,'editroute.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editroute_post(request):
    fd = request.POST['from_destination']
    td = request.POST['to_destination']
    lt = request.POST['latitude']
    lg = request.POST['longitude']
    id=request.POST['id']
    i = Route.objects.get(id=id)
    i.from_destination = fd
    i.to_destination = td
    i.latitude = lt
    i.longititude = lg
    i.save()

    return redirect('/myapp/viewroute/')

@login_required(login_url='/myapp/login_get/')
def deleteroute(request,id):
    data=Route.objects.get(id=id)
    data.delete()
    return redirect('/myapp/viewroute/')

@login_required(login_url='/myapp/login_get/')
def addstop_get(request):
    data=Route.objects.all()
    return render(request,'addstop.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def addstop_post(request):
    route=request.POST['route']
    stop=request.POST['stopname']
    i=Stop()
    i.ROUTE=Route.objects.get(id=route)
    i.stopname=stop
    i.save()
    return redirect('/myapp/viewstop/')

@login_required(login_url='/myapp/login_get/')
def viewstop(request):
    data=Stop.objects.all()
    return render(request,'viewstop.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def editstop_get(request,id):
    r=Route.objects.all()
    data=Stop.objects.get(id=id)
    return render(request,'editstop.html',{'data':data,'ro':r})

@login_required(login_url='/myapp/login_get/')
def editstop_post(request):
    n=request.POST['route']
    stopname=request.POST['stopname']
    id=request.POST['id']
    i=Stop.objects.get(id=id)
    i.ROUTE=Route.objects.get(id=n)
    i.stopname=stopname
    i.save()
    return redirect('/myapp/viewstop/')

@login_required(login_url='/myapp/login_get/')
def deletestop(request,id):
    data=Stop.objects.get(id=id)
    data.delete()
    return redirect('/myapp/viewstop/')

@login_required(login_url='/myapp/login_get/')
def assignroute_get(request):
    data=Bus.objects.all()
    r=Route.objects.all()
    return render(request,'assignroute.html',{'data':data,'rot':r})

@login_required(login_url='/myapp/login_get/')
def assignroute_post(request):
    b=request.POST['bus']
    r=request.POST['route']
    i=Assign_route()
    i.BUS=Bus.objects.get(id=b)
    i.ROUTE=Route.objects.get(id=r)
    i.save()

    return redirect('/myapp/viewassignroute/')

@login_required(login_url='/myapp/login_get/')
def view_assignroute(request):
    data=Assign_route.objects.all()
    return render(request,'viewassignroute.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def addplace_get(request):
    data = Stop.objects.select_related('ROUTE').all()
    return render(request, 'addplace.html', {'data': data})

@login_required(login_url='/myapp/login_get/')
def addplace_post(request):
    stop=request.POST['stop']
    placen=request.POST['placename']
    lat=request.POST['latitude']
    lon=request.POST['longitude']
    plty=request.POST['placetype']
    i=Place()
    i.stop=Stop.objects.get(id=stop)
    i.placename=placen
    i.latitude=lat
    i.longitude=lon
    i.placetype=plty
    i.save()
    return redirect('/myapp/viewplace/')

@login_required(login_url='/myapp/login_get/')
def viewplace(request):
    i=Place.objects.all()
    return render(request,'viewplace.html',{'data':i})

@login_required(login_url='/myapp/login_get/')
def editplace_get(request,id):
    stop=Stop.objects.all()
    i=Place.objects.get(id=id)
    return render(request,'editplace.html',{'data':i,'st':stop})

@login_required(login_url='/myapp/login_get/')
def editplace_post(request):
    stop=request.POST['stop']
    placename=request.POST['placename']
    latitude=request.POST['latitude']
    longitude=request.POST['longitude']
    placetype=request.POST['placetype']
    id=request.POST['id']
    i=Place.objects.get(id=id)
    i.stop=Stop.objects.get(id=stop)
    i.placename=placename
    i.latitude=latitude
    i.longititude=longitude
    i.placetype=placetype
    i.save()
    return redirect('/myapp/viewplace/')

@login_required(login_url='/myapp/login_get/')
def deleteplace(request,id):
    i=Place.objects.get(id=id)
    i.delete()
    return redirect('/myapp/viewplace/')


# ======================================================================================================================================
@csrf_exempt
def registeruser_post(request):
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        place=request.POST['place']
        city=request.POST['city']
        district=request.POST['district']
        pin=request.POST['pin']
        pwd=request.POST['password']

        if User.objects.filter(username=email).exists():
            return JsonResponse({'status':'error','message':'email is already exist'})

        u=User.objects.create_user(username=email,password=pwd)
        group=Group.objects.get(name='users')
        u.groups.add(group)
        u.save()

        i=user()
        i.name=name
        i.email=email
        i.phone=phone
        i.place=place
        i.city=city
        i.district=district
        i.pin=pin
        i.Auth_USER=u
        i.save()

        return JsonResponse({'status':'ok'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email).first()
        if user_obj is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Incorrect email'
            })

        user = authenticate(username=email, password=password)
        if user is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Incorrect password'
            })

        if user.groups.filter(name='users').exists():
            return JsonResponse({
                'status': 'ok',
                'lid': user.id,
                'type': 'admin'   # OR 'users' if you want
            })

        elif user.groups.filter(name='authority').exists():
            return JsonResponse({
                'status': 'ok',
                'lid': user.id,
                'type': 'authority'
            })

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'User not allowed'
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })

@csrf_exempt
def viewbus_user(request):
    try:
        bus = Bus.objects.all()
        data = []

        for i in bus:
            data.append({
                "id": i.id,
                "busname": i.bus_name,
                "regno": i.reg_no,
                "ownername": i.ownername,
                "owneremail": i.owneremail,
            })

        return JsonResponse({
            "status": "ok",
            "data": data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

@csrf_exempt
def view_route_user(request):
    try:
        routes = Route.objects.all()
        data = []

        for i in routes:
            data.append({
                'id': i.id,
                'fdestination': i.from_destination,
                'tdestination': i.to_destination,
                'latitude': i.latitude,
                'longitude': i.longititude
            })


        return JsonResponse({
            'status': 'ok',
            'data': data
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@csrf_exempt
def view_stop_user(request):
    try:
        stops = Stop.objects.select_related('ROUTE').all()

        data = []

        for i in stops:
            data.append({
                'id': i.id,
                'stopname': i.stopname,

                # route details
                'route_from': i.ROUTE.from_destination,
                'route_to': i.ROUTE.to_destination,

                # combined route (easy for UI)
                'route': f"{i.ROUTE.from_destination} → {i.ROUTE.to_destination}"
            })

        return JsonResponse({
            'status': 'ok',
            'data': data
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
@csrf_exempt
def view_place_user(request):
    try:
        place=Place.objects.all()

        data=[]

        for i in place:
            data.append({
                'id':i.id,
                'stop':i.stop.stopname,
                'placename':i.placename,
                'latitude':i.latitude,
                'longitude':i.longitude,
                'placetype':i.placetype
            })

        return JsonResponse({
                'status':'ok',
                'data':data
            })

    except Exception as e:
        return JsonResponse({
            'status':'error',
            'message':str(e)
        })

@csrf_exempt
def send_complaint(request):
    id=request.POST['lid']
    print(id)
    complaint=request.POST['complaint']
    obj=Complaint()
    obj.date = datetime.now().date()
    obj.complaint = complaint
    obj.reply='pending'
    obj.status='pending'
    obj.USER = usersprofile.objects.get(Auth_USER_id=id)
    obj.save()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def view_complaints(request, lid):
    try:
        complaints = Complaint.objects.filter(
            USER__Auth_USER_id=lid
        ).order_by("-id").values(
            "complaint",
            "reply",
            "status",
            "date"
        )

        return JsonResponse(list(complaints), safe=False)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })


@csrf_exempt
def authority_complaints(request):
    if request.method != "GET":
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"},
            status=405
        )

    try:
        complaints = Complaint.objects.all().order_by("-id")

        data = []
        for c in complaints:
            data.append({
                "id": c.id,
                "user_id": c.USER.id,
                "complaint": c.complaint,
                "reply": c.reply if c.reply else "",
                "status": c.status,
                "date": c.date,   # ✅ CharField – safe
            })

        return JsonResponse({"complaints": data}, status=200)

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )


@csrf_exempt
def authority_send_reply(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"},
            status=405
        )

    try:
        body = json.loads(request.body)
        cid = body.get("complaint_id")
        reply = body.get("reply")

        if not cid or not reply:
            return JsonResponse(
                {"status": "error", "message": "Missing data"},
                status=400
            )

        complaint = Complaint.objects.get(id=cid)
        complaint.reply = reply
        complaint.status = "replied"
        complaint.save()

        return JsonResponse({"status": "success"}, status=200)

    except Complaint.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Complaint not found"},
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )



@csrf_exempt
def predict_risk_api(request):
    if request.method == "POST":
        try:
            lat = float(request.POST.get("latitude"))
            lon = float(request.POST.get("longitude"))
        except (TypeError, ValueError):
            return JsonResponse({
                "status": "error",
                "message": "Invalid latitude or longitude"
            })

        result = predict_risk(lat, lon)
        return JsonResponse(result)

    return JsonResponse({
        "status": "error",
        "message": "Only POST method allowed"
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.utils import predict_risk


@csrf_exempt
def predict_risk_view(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"},
            status=400
        )

    try:
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")

        if not lat or not lon:
            return JsonResponse(
                {"status": "error", "message": "Latitude and longitude required"},
                status=400
            )

        lat = float(lat)
        lon = float(lon)

        result = predict_risk(lat, lon)

        # If no data found
        if result.get("status") != "success":
            return JsonResponse(result)

        # ✅ Keep SAME response structure (frontend safe)
        return JsonResponse({
            "status": "success",
            "nearest_place": result["nearest_place"],
            "risk_level": result["predicted_risk"],
            "distance_km": result["distance_km"],
            "crime_count": result["crime_count"],
            "average_risk": result["average_risk"],
            "crime_types": result.get("crime_types", [])
        })

    except ValueError:
        return JsonResponse(
            {"status": "error", "message": "Invalid latitude or longitude"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )

@csrf_exempt
def send_alert(request):
        if request.method == "POST":
            data = json.loads(request.body)

            user_id = data['user_id']
            latitude = data['latitude']
            longitude = data['longitude']

            user = User.objects.get(id=user_id)

            Alert.objects.create(
                USER=user,
                message="Danger",
                latitude=latitude,
                longitude=longitude,
                date=datetime.now().date(),
                time=datetime.now().time()
            )

            return JsonResponse({
                "status": "ok",
                "message": "Alert sent successfully"
            })

        return JsonResponse({"status": "error"})

import random

@csrf_exempt
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(username=email)

            # Generate new password
            new_pass = str(random.randint(100000, 999999))

            # Save encrypted password
            user.password = make_password(new_pass)
            user.save()

            # Email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "threatdetectionids@gmail.com"
            app_password = "cmfncqscvacvvkjf"

            subject = "Password Reset - Courier Management"
            body = f"""
Hello,

Your new password is: {new_pass}

Please login and change your password.

Safecity System
"""

            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Send Email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email, message.as_string())
            server.quit()

            return JsonResponse({
                'status': 'ok',
                'message': 'New password sent to your email'
            })

        except User.DoesNotExist:

            return JsonResponse({
                'status': 'error',
                'message': 'Email not found'
            })

        except Exception as e:

            return JsonResponse({
                'status': 'error',
                'message': f'Email send error: {str(e)}'
            })

@csrf_exempt
def view_alerts(request):

    alerts = Alert.objects.all().order_by('-date','-time')

    data=[]

    for a in alerts:

        data.append({

            "id":a.id,
            "user":a.USER.username,
            "message":a.message,
            "date":str(a.date),
            "time":str(a.time),
            "latitude":a.latitude,
            "longitude":a.longitude

        })

    return JsonResponse({"status":"ok","data":data})


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from myapp.utils import predict_risk,haversine
#
# @csrf_exempt
# def predict_risk_view(request):
#     data = json.loads(request.body)
#     user_lat = float(data['latitude'])
#     user_lon = float(data['longitude'])
#
#     df = pd.read_csv("ernakulam_crime_data.csv")
#
#     nearby = []
#     crimes = set()   # 👈 crime list
#
#     for _, row in df.iterrows():
#         dist = haversine(
#             user_lat, user_lon,
#             row['latitude'], row['longitude']
#         )
#
#         if dist <= 4:  # 4 km radius
#             nearby.append(row)
#             crimes.add(row['crime_type'])  # 👈 collect crime
#
#     if not nearby:
#         return JsonResponse({
#             "risk_level": "LOW",
#             "nearest_place": "No crime nearby",
#             "crimes": []
#         })
#
#     crime_count = len(nearby)
#
#     if crime_count > 10:
#         risk = "HIGH"
#     elif crime_count > 4:
#         risk = "MEDIUM"
#     else:
#         risk = "LOW"
#
#     return JsonResponse({
#         "risk_level": risk,
#         "nearest_place": "Nearby Area",
#         "crimes": list(crimes)   # 👈 SEND TO FLUTTER
#     })
