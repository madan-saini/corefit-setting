from django.shortcuts import render
from .. models import *
from django.http import HttpResponse, JsonResponse
import random
import string
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from django.shortcuts import render
import datetime as date
from django.core.files.storage import FileSystemStorage
from django.db import connection
from ..controller.send_email import *
import os
from django.conf import settings
from django.core.mail import *
import math
from django.contrib.auth.hashers import make_password
# import random
from django.contrib.auth.hashers import *
from django.core.signing import Signer
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.text import slugify
import json
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from smtplib import SMTP 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import get_template
import requests
from flask import render_template, make_response, redirect
from django import forms


# Create your views here.
env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))


def basicProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES
    print(data)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    training_type = data.get("training_type")
    languages_array = data.getlist("languages")
    languages = ",".join(languages_array)
    year_of_experince = data.get("year_of_experince")
    dob = data.get("dob")
    gender = data.get("gender")
    try:
        if bool(dob):
            date_val = date.datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        date_val = ''
    User.objects.filter(id=user_id).update(dob=date_val, first_name=first_name, last_name=last_name,languages=languages,year_of_experince=year_of_experince,gender=gender)
    website = data.get("website")
    about = data.get("about")
    short_bio = data.get("short_bio")
    location = data.get("location")
    homelocation = data.get("homelocation")
    country = data.get("country")
    nationality = data.get("nationality")
    city = data.get("city")
    key_skills_arr = data.getlist("key_skills")
    height = data.get("height")
    height_type_1 = data.get("height_type_1")
    weight = data.get("weights")
    weight_type_1 = data.get("weight_type_1")
    key_skills_arr = data.getlist("key_skills")
    key_skills = ",".join(key_skills_arr)
    old_bio_video = data.get("old_bio_video")
    other_skills_arr = data.getlist("other_skills")
    other_skills = ",".join(other_skills_arr)
    basic_info_id = data.get("basic_info_id")
    file_name = old_bio_video
    try:
        train_country2 = data.get("train_country2")
        train_city2 = data.get("train_city2")
        trainlocation2 = data.get("trainlocation2")
        homelocation2 = data.get("homelocation2")
    except:
        train_country2 = ''
        train_city2 = ''
        trainlocation2 = ''
        homelocation2 = ''
    location_train = data.getlist("tlocation")
    update_train = data.getlist("updateloc")

    loca=''
    dictTrain = {}
    TrainingLocation.objects.filter(user_id=user_id).delete()
    for loc in location_train:
        if loc:
            loca = TrainingLocation(
                user_id = user_id,
                training_locations = loc,
                slug=''.join(random.choice(string.ascii_letters) for _ in range(15))
            )
            loca.save()


    # print("weight",weight)
    # print("weight_type_1",weight_type_1)
    if files:
        fss = FileSystemStorage()
        bio_video = files['bio_video']
        # print(bio_video)
        file_name = str(bio_video)
        file = fss.save('static/uploads/bioVideo/' + str(bio_video), bio_video)
    # print(basic_info_id)

    if basic_info_id != '':
        basicInfo = BasicInfo(
            id=basic_info_id,
            user_id=user_id,
            website=website,
            about=about,
            short_bio=short_bio,
            location=location,
            homelocation=homelocation,
            homelocation2=homelocation2,
            trainlocation2=trainlocation2,
            train_city2=train_city2,
            train_country2=train_country2,
            training_type=training_type,
            nationality=nationality,
            country_id=country,
            height=height,
            height_type_1=height_type_1,
            weight=weight,
            weight_type_1=weight_type_1,
            city=city,
            bio_video=file_name,
            key_skills=key_skills,
            other_skills=other_skills,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    else:
        basicInfo = BasicInfo(
            user_id=user_id,
            website=website,
            about=about,
            short_bio=short_bio,
            location=location,
            nationality=nationality,
            training_type=training_type,
            homelocation=homelocation,
            height=height,
            homelocation2=homelocation2,
            trainlocation2=trainlocation2,
            train_city2=train_city2,
            train_country2=train_country2,
            height_type_1=height_type_1,
            weight=weight,
            weight_type_1=weight_type_1,
            country_id=country,
            city=city,
            key_skills=key_skills,
            other_skills=other_skills,
            bio_video=file_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    # print(basicInfo)
    basicInfo.save()
    context = {
        0: basicInfo.id, 1: "facility_profile_level",2:basicInfo.bio_video
    }
    return JsonResponse(context)
def deleteLocation(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    TrainingLocation.objects.filter(id=id).delete()
    return HttpResponse(1)

def awardProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES

    award_name = data.get("award_name")
    location = data.get("award_location")
    award_date = data.get("award_date")
    file_name = ''
    date_val = ''

    try:
        if bool(files['award_document']):
            award_document = files['award_document']
    except:
        award_document = ''

    try:
        if bool(award_date):
            date_val = date.datetime.strptime(award_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        date_val = ''

    if award_document:
        fss = FileSystemStorage()
        # print(award_document)
        # fileExtension = os.path.splitext(str(award_document))
        # print(fileExtension)
        # ext = award_document.split(".")[-1]
        # file_name = award_document
        # print(os.path.splitext(file_name))
        file_name = rand_slug() + "-" + str(award_document) 
        file = fss.save('static/uploads/documents/'+file_name, award_document)
        file_url = fss.url(file)

    awards = UserAward(
        user_id=user_id,
        award_name=award_name,
        location=location,
        document=file_name,
        status=1,
        date=date_val,
        
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    awards.save()

    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    context = {
        'awardList': awardInfo,
    }

    return render(request, 'frelancerTemplates/elements/users/award_table.html', context)


def deleteAward(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    UserAward.objects.filter(id=id).delete()
    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()
    context = {
        'awardList': awardInfo,
    }

    return render(request, 'elements/users/award_table.html', context)



def viewAward(request):
    data = request.POST

    id = data.get("id")
    awardValue = UserAward.objects.get(id=id)

    countries = Country.objects.all().values_list('id', 'name').order_by('name')

    context = {
        'awardValue': awardValue,
        'countries': countries,
    }

    return render(request, 'frelancerTemplates/elements/users/award_model.html', context)


def editAwardProfile(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES

    # print(data)
    # print(files)

    award_name = data.get("award_title")
    location = data.get("award_location")
    award_date = data.get("award_date")
    id = data.get("award_id")

    file_name = data.get("old_award_document")
    if files:
        fss = FileSystemStorage()
        award_document = files['edit_award_document']
        file_name = rand_slug() + "-" + str(award_document)
        file = fss.save('static/uploads/documents/' + file_name, award_document)
        file_url = fss.url(file)

    awards = UserAward(
        id=id,
        user_id=user_id,
        award_name=award_name,
        location=location,
        document=file_name,
        date=date.datetime.strptime(award_date, "%d/%m/%Y").strftime("%Y-%m-%d"),

        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    awards.save()

    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    context = {
        'awardList': awardInfo,
    }

    return render(request, 'frelancerTemplates/elements/users/award_table.html', context)


def identityForm(request):
    user_id = request.session['user_id']
    data = request.POST
    files = request.FILES
    # print(data)

    terms = 1
    old_business_doc = data['old_business_doc']
    old_director_doc = data['old_director_doc']

    try:
        business_doc = files['business_doc']
        fss = FileSystemStorage()
        business_doc_name = rand_slug() + "-" + str(business_doc)
        file_image = fss.save('static/uploads/documents/' + business_doc_name, business_doc)
    except:
        business_doc_name = old_business_doc

    try:
        director_doc = files['director_doc']
        fss = FileSystemStorage()
        director_doc_name = rand_slug() + "-" + str(director_doc)
        file_image = fss.save('static/uploads/documents/' + director_doc_name, director_doc)
    except:
        director_doc_name = old_director_doc

    User.objects.filter(id=user_id).update(terms=terms, business_doc=business_doc_name, director_doc=director_doc_name,
                                           updated_at=datetime.utcnow())

    return HttpResponse(1)

def association(request):
    user_id = request.session['user_id']
    data = request.POST
    gymslect=data['gymslect']
    userdata = User.objects.filter(id=user_id).values()
    userdata.freelance_id = user_id
    slug= ''.join(random.choice(string.ascii_letters) for _ in range(15))
    cursor = connection.cursor()

    from django.db.models import Q

    try:
        chck = data['chboxSt']
    except:
        chck = ''
    if chck != '':
        return HttpResponse(2)
    # user_type = "Personal Trainer"
    if data['gymslect']:        
        if Branch.objects.filter(id=gymslect):
            branchInfo = Branch.objects.get(id=gymslect)

        # cursor.execute(
        #     "INSERT INTO `users` (user_type,freelance_id,twitterLink,instagramLink,facebookLink,first_name,last_name,email_address,password,contact,nationality,dob,languages ,height,weight,gender,year_of_experince,allow_promotion,identification,business_doc,director_doc,uniqueKey,terms ,slug,status, created_at, updated_at) SELECT'" +user_type+ "','" +
        #     str(user_id) + "', twitterLink,instagramLink,facebookLink,first_name,last_name,email_address,password,contact,nationality,dob,languages ,height,weight,gender,year_of_experince,allow_promotion,identification,business_doc,director_doc,uniqueKey,terms,'" + slug + "',status,  '" + str(
        #         datetime.utcnow()) + "', '" + str(
        #         datetime.utcnow()) + "' FROM `users` where id = " + str(user_id) + "")

        request1 = Request(
            freelancer_user_id=user_id,
            type = 'Association',
            association_id = gymslect,
            gym_user_id = branchInfo.user_id,
            status=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        request1.save()
    # return HttpResponse(1)
    branc = BasicInfo.objects.all().filter(Q(facility_profile_level ="Both")| Q(facility_profile_level ="Branch")).select_related("user")

    if bool(Request.objects.filter(freelancer_user_id=user_id,status=0)):
        isRequest = Request.objects.get(freelancer_user_id=user_id,status=0)

    context = {
        "isRequest":isRequest,
        "branc":branc
    }

    return render(request, 'frelancerTemplates/elements/myProfile/update_association.html', context)

def employeeRequests(request):
    user_id = request.session['user_id']

    from datetime import timedelta
    title = 'Request'

    records = Request.objects.all().filter(freelancer_user_id=user_id,type='Employee Request').select_related('freelancer_user','gym_user')

    # dat = User.objects.filter(email_address="pt1@mailinator.com").values()
    # dat = BasicInfo.objects.filter(id = 54).prefetch_related('country_set')
    # print(dat.country_set)
    
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

    return render(request, 'frelancerTemplates/users/requests.html', context)

def viewInviteRequest(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    requestData = Request.objects.get(id=id)
    
    context = {
        'requestData': requestData,
    }
    
    return render(request, 'frelancerTemplates/elements/users/request_popup.html', context)

def changeInviteRequestStatus(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    type = data.get("type")
    from datetime import timedelta

    requestData = Request.objects.get(id=id)
    if type == 'Accept':
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
    
    records = Request.objects.all().filter(freelancer_user_id=user_id).select_related('gym_user','freelancer_user')

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

    return render(request, 'frelancerTemplates/elements/users/request_table.html', context)

def searchInviteRequest(request):
    user_id = request.session['user_id']
    data = request.POST

    from datetime import timedelta

    search = data.get("search")

    if data.get("search_status"):
        search_status = data.getlist("search_status")
    else :
        search_status = ''
    # search_location = data.get("search_location")
    search_start_date = data.get("search_start_date")
    search_end_date = data.get("search_end_date")
    from django.db.models import Q, CharField, Value as V
    from django.db.models.functions import Concat  

    # print(search_status)
    # print(search_start_date)
    # print(search_end_date)
    con2 = con3 = con4 = con5 = Q()
    if search_status != '':  
        con2 = Q(status__in=search_status) #any query you want
    # if search_location != '':
        # con3 = Q(freelancer_user__location__contains = search_location) #any query you want
    if search_start_date != '' and search_end_date != '':
        con4 = Q(created_at__gte = search_start_date) #any query you want
        con5 = Q(created_at__lte = search_end_date) #any query you want
    
    records = Request.objects.all().annotate(C=Concat('freelancer_user__first_name', V(' '), 'freelancer_user__last_name', output_field=CharField())).filter(freelancer_user_id = user_id,type='Employee Request').filter(
            Q(C__icontains=search.lower()) | Q(freelancer_user__email_address__contains = search.lower()) | Q(freelancer_user__id__contains = search.lower())).filter(con2 & con3 & con4 & con5).select_related('freelancer_user','gym_user')
        
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

    return render(request, 'frelancerTemplates/elements/users/request_table.html', context)

def disassociation(request):
    user_id = request.session['user_id']
    data = request.POST

    disassociate_id = data['disassociate_id']
    userData = User.objects.filter(freelance_id=disassociate_id).values().first()
    
    gym_user_id = userData['user_id']

    
    request = Request(
        freelancer_user_id=user_id,
        type = 'Disassociation',
        gym_user_id = gym_user_id,
        status=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    request.save()

    return HttpResponse(1)

def cancelAssociation(request):
    data = request.POST
    user_id = request.session['user_id']

    id = data.get("id")
    from django.db.models import Q

    Request.objects.filter(id=id).update(status=3)
    
    branc = BasicInfo.objects.all().filter(Q(facility_profile_level ="Both")| Q(facility_profile_level ="Branch")).select_related("user")

    context = {
        "isRequest":'',
        "branc":branc
    }

    return render(request, 'frelancerTemplates/elements/myProfile/update_association.html', context)