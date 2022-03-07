from locale import currency
from django.shortcuts import render
from .. models import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django import template
from django.core.mail import *
import math
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.hashers import *
from django.core.signing import Signer
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import random
from django.utils.text import slugify
import string
import json
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from smtplib import SMTP 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from django.template.loader import get_template
from . send_email import *
import requests
import datetime as date
from flask import render_template, make_response, redirect
from django.shortcuts import render  
from django import forms
from django.db import connection
from django.db.models import Q, Avg, Count, Aggregate

from requests import get
import numpy as np


from django.core.files.storage import FileSystemStorage

import os
# Create your views here.

env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def employeeRequest(request):
    user_id = request.session['user_id']

    title = settings.SITE_TITLE + ' | ' + 'Employee Request'

    records = Request.objects.all().filter(gym_user_id=user_id).filter(Q(type='Association') | Q(type='Disassociation')).select_related('gym_user','freelancer_user')

    request_type = (('Association','Association'),('Disassociation','Disassociation'))
    end = date.datetime.now()
    start = date.datetime.now() - timedelta(days=60)
    context = {
        'pageTitle': title,
        'user_id': user_id,
        'records': records,
        'request_type': request_type,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'requests/employee-request.html', context)

def viewRequest(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    requestData = Request.objects.get(id=id)
    
    context = {
        'requestData': requestData,
    }
    
    return render(request, 'elements/employee-request/request_popup.html', context)

def changeRequestStatus(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    type = data.get("type")
    request_type = data.get("request_type")


    if request_type == 'Association':
        if type == 'Accept':
            requestData = Request.objects.get(id=id)
            gym_id = requestData.gym_user_id
            pt_id = requestData.freelancer_user_id
            slug= ''.join(random.choice(string.ascii_letters) for _ in range(15))
            user_type = "Personal Trainer"

            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO `users` (user_type,freelance_id,user_id,twitterLink,instagramLink,facebookLink,first_name,last_name,email_address,password,contact,nationality,dob,languages ,height,weight,gender,year_of_experince,allow_promotion,identification,business_doc,director_doc,uniqueKey,terms ,slug,status, created_at, updated_at) SELECT'" +user_type+ "','" +
                str(pt_id) + "','" + str(gym_id) + "', twitterLink,instagramLink,facebookLink,first_name,last_name,email_address,password,contact,nationality,dob,languages ,height,weight,gender,year_of_experince,allow_promotion,identification,business_doc,director_doc,uniqueKey,terms,'" + slug + "',status,  '" + str(
                    datetime.utcnow()) + "', '" + str(
                    datetime.utcnow()) + "' FROM `users` where id = " + str(pt_id) + "")

            Request.objects.filter(id=id).update(status=1)
        else:
            Request.objects.filter(id=id).update(status=2)
    else:
        if type == 'Accept':
            requestData = Request.objects.get(id=id)
            gym_id = requestData.gym_user_id
            pt_id = requestData.freelancer_user_id
            userData = User.objects.filter(freelance_id=pt_id).values().first()
            employeeId = userData['id']

            User.objects.filter(id=employeeId).update(user_id=0, updated_at=datetime.utcnow())
            Request.objects.filter(id=id).update(status=1)
        else:
            Request.objects.filter(id=id).update(status=2)
    
    records = Request.objects.all().filter(gym_user_id=user_id).filter(Q(type='Association') | Q(type='Disassociation')).select_related('gym_user','freelancer_user')

    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)
    context = {
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'elements/employee-request/request-table.html', context)

def searchRequest(request):
    user_id = request.session['user_id']
    data = request.POST
    # print(data)

    search = data.get("search")

    if data.get("search_status"):
        search_status = data.getlist("search_status")
    else :
        search_status = ''
    if data.get("search_type"):
        search_type = data.getlist("search_type")
    else :
        search_type = ''
    # search_location = data.get("search_location")
    search_start_date = data.get("search_start_date")+' 00:00:00'
    search_end_date = data.get("search_end_date")+' 23:59:59'
    from django.db.models import F, CharField, Value as V
    from django.db.models.functions import Concat  

    con2 = con3 = con4 = con5 = Q()
    if search_status != '':  
        con2 = Q(status__in=search_status) #any query you want
    if search_type != '':  
        con3 = Q(type__in=search_type) #any query you want
    # if search_location != '':
        # con3 = Q(freelancer_user__location__contains = search_location) #any query you want
    if search_start_date != '' and search_end_date != '':
        con4 = Q(created_at__range=(search_start_date, search_end_date))
        # con4 = Q(created_at__gte = search_start_date) #any query you want
        # con5 = Q(created_at__lte = search_end_date) #any query you want
    
    records = Request.objects.all().annotate(C=Concat('freelancer_user__first_name', V(' '), 'freelancer_user__last_name', output_field=CharField())).filter(gym_user_id = user_id).filter(Q(type='Association') | Q(type='Disassociation')).filter(
            Q(C__icontains=search.lower()) | Q(freelancer_user__email_address__contains = search.lower()) | Q(freelancer_user__id__contains = search.lower())).filter(con2 & con3 & con4 & con5).select_related('gym_user','freelancer_user')
    
    # print(records.query)

    end = date.datetime.now()
    start = date.datetime.now() - timedelta(days=60)
    context = {
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'elements/employee-request/request-table.html', context)

def inviteEmployee(request):
    user_id = request.session['user_id']

    title = settings.SITE_TITLE + ' | ' + 'Invite Employee'

    records = Request.objects.all().filter(gym_user_id=user_id,type='Employee Request').select_related('gym_user','freelancer_user')
    

    end = date.datetime.now()
    start = date.datetime.now() - timedelta(days=60)
    context = {
        'pageTitle': title,
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'requests/invite-employee.html', context)

def addPersonalTrainer(request):
    user_id = request.session['user_id']

    title = 'Invite Employee'

    records = Request.objects.all().filter(gym_user_id=user_id).select_related('gym_user','freelancer_user')

    start = date.datetime.now()
    end = date.datetime.now() + timedelta(days=60)
    context = {
        'pageTitle': title,
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'requests/add-personal-trainer.html', context)

def searchTrainer(request):
    user_id = request.session['user_id']
    data = request.POST

    from django.db.models import F, CharField, Value as V
    from django.db.models.functions import Concat

    search = data.get("name")

    records = BasicInfo.objects.all().annotate(C=Concat('user__first_name', V(' '), 'user__last_name', output_field=CharField())).filter(
            Q(C__icontains=search.lower()) | Q(user__id__contains = search.lower()) | Q(user__email_address__contains = search.lower())).filter(user__user_type='FreelanceTrainer')
    # print(records.query)
    reqListIds = Request.objects.filter(gym_user_id=user_id,status=0).values_list('freelancer_user_id', flat=True)

    context = {
        'user_id': user_id,
        'reqListIds': list(reqListIds),
        'records': records
    }

    return render(request, 'elements/employee-request/trainer-table.html', context)

def addTrainer(request):
    user_id = request.session['user_id']
    data = request.POST

    if data.getlist("selected_record"):
        for uId in data.getlist("selected_record"):
            record = Request(
                gym_user_id=user_id,
                freelancer_user_id=uId,
                association_id = 0,
                type='Employee Request',
                status=0,

                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            record.save()

    return HttpResponse(1)

def viewInviteRequest(request):
    data = request.POST
    user_id = request.session['user_id']

    eid = data.get("id")

    requestData = Request.objects.get(id=eid)
    context = {
        'requestData': requestData,
    }
    
    return render(request, 'elements/employee-request/invite_popup.html', context)

def searchSPRequest(request):
    user_id = request.session['user_id']
    data = request.POST

    search = data.get("search")

    if data.get("search_status"):
        search_status = data.getlist("search_status")
    else :
        search_status = ''
    # search_location = data.get("search_location")
    search_start_date = data.get("search_start_date")+' 00:00:00'
    search_end_date = data.get("search_end_date")+' 23:59:59'
    from django.db.models import F, CharField, Value as V
    from django.db.models.functions import Concat  

    con2 = con3 = con4 = con5 = Q()
    if search_status != '':  
        con2 = Q(status__in=search_status) #any query you want
    # if search_location != '':
        # con3 = Q(freelancer_user__location__contains = search_location) #any query you want
    if search_start_date != '' and search_end_date != '':
        con4 = Q(created_at__gte = search_start_date) #any query you want
        con5 = Q(created_at__lte = search_end_date) #any query you want
    
    records = Request.objects.all().annotate(C=Concat('freelancer_user__first_name', V(' '), 'freelancer_user__last_name', output_field=CharField())).filter(gym_user_id = user_id,type='Employee Request').filter(
            Q(C__icontains=search.lower()) | Q(freelancer_user__email_address__contains = search.lower()) | Q(freelancer_user__id__contains = search.lower())).filter(con2 & con3 & con4 & con5).select_related('freelancer_user','gym_user')
        

    end = date.datetime.now()
    start = date.datetime.now() - timedelta(days=60)
    context = {
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'elements/employee-request/invite-table.html', context)

def cancelRequestStatus(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    type = data.get("type")

    Request.objects.filter(id=id).update(status=3)
    
    records = Request.objects.all().filter(gym_user_id=user_id).select_related('freelancer_user','gym_user')

    end = date.datetime.now()
    start = date.datetime.now() - timedelta(days=60)
    context = {
        'user_id': user_id,
        'records': records,
        'start': start.strftime("%d/%m/%Y"),
        'end':end.strftime("%d/%m/%Y"),
        'startV': start.strftime("%Y-%m-%d"),
        'endV':end.strftime("%Y-%m-%d"),
    }

    return render(request, 'elements/employee-request/invite-table.html', context)
