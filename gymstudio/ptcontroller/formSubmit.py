from django.shortcuts import render
from .. models import *
from django.http import HttpResponse, JsonResponse
import random
import string
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import datetime as date
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from ..controller.send_email import *


from django.core.mail import *
from django.contrib.auth.hashers import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher


# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))


def basicProfile(request):
    user_id = request.session['user_id']
    user_id2 = request.session['user_id']
    data = request.POST
    files = request.FILES
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
    basic_info_id2 = data.get("basic_info_id2")
    file_name = old_bio_video
    # print("weight",weight)
    # print("weight_type_1",weight_type_1)
    if files:
        fss = FileSystemStorage()
        bio_video = files['bio_video']
        # print(bio_video)
        file_name = str(bio_video)
        file = fss.save('static/uploads/bioVideo/' + str(bio_video), bio_video)
    frUser_id = user_id
    basicInfo2=''
    if basic_info_id2 != '' :
        BasicInfo.objects.filter( id=basic_info_id2).update(
            training_type=training_type,
            nationality=nationality,
            height=height,
            height_type_1=height_type_1,
            weight=weight,
            weight_type_1=weight_type_1,
            updated_at=datetime.utcnow(),
        )
        basicInfo2 = BasicInfo.objects.get(id=basic_info_id2)

    else:
        basicInfo2 = BasicInfo(
            user_id=user_id,
            training_type=training_type,
            nationality=nationality,
            height=height,
            height_type_1=height_type_1,
            weight=weight,
            weight_type_1=weight_type_1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        basicInfo2.save()
    user = User.objects.get(freelance_id=user_id)

    user_id = user.id
    basicInfo = ''
    if basic_info_id != '' :

       BasicInfo.objects.filter( id=basic_info_id).update(
            website=website,
            about=about,
            short_bio=short_bio,
            location=location,
            homelocation=homelocation,
            training_type=training_type,
            country=country,
            nationality=nationality,
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
       basicInfo = BasicInfo.objects.get(id=basic_info_id)

    else:
        basicInfo = BasicInfo(
            user_id=user_id,
            website=website,
            about=about,
            short_bio=short_bio,
            location=location,
            training_type=training_type,
            homelocation=homelocation,
            height=height,
            height_type_1=height_type_1,
            weight=weight,
            weight_type_1=weight_type_1,
            country=country,
            nationality=nationality,
            city=city,
            key_skills=key_skills,
            other_skills=other_skills,
            bio_video=file_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        basicInfo.save()

   
    context = {
        0: basicInfo.id, 1: "facility_profile_level",2:basicInfo.bio_video,3:basicInfo2.id
    }
    return JsonResponse(context)

def awardProfile(request):
    user_id = request.session['user_id']
    user = User.objects.get(freelance_id=user_id)
    user_id = user.id
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

    return render(request, 'ptTemplates/elements/users/award_table.html', context)


def deleteAward(request):
    data = request.POST
    user_id = request.session['user_id']
    data = request.POST

    id = data.get("id")
    UserAward.objects.filter(id=id).delete()
    user = User.objects.get(freelance_id=user_id)
    user_id = user.id
    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()
    context = {
        'awardList': awardInfo,
    }

    return render(request, 'ptTemplates/elements/users/award_table.html', context)
def viewAward(request):
    data = request.POST
    data = request.POST

    id = data.get("id")
    awardValue = UserAward.objects.get(id=id)

    countries = Country.objects.all().values_list('id','name').order_by('name')

    context = {
        'awardValue': awardValue,
        'countries': countries,
    }
    
    return render(request, 'ptTemplates/elements/users/award_model.html', context)

def editAwardProfile(request):
    user_id = request.session['user_id']
    user = User.objects.get(freelance_id=user_id)
    user_id = user.id
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
        file = fss.save('static/uploads/documents/'+file_name, award_document)
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

    return render(request, 'ptTemplates/elements/users/award_table.html', context)

def identityForm(request):
    user_id = request.session['user_id']
    # user = User.objects.get(freelance_id=user_id)
    # user_id = user.id
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
        file_image = fss.save('static/uploads/documents/'+business_doc_name, business_doc)
    except:
        business_doc_name = old_business_doc

    try:
        director_doc = files['director_doc']
        fss = FileSystemStorage()
        director_doc_name = rand_slug() + "-" + str(director_doc)
        file_image = fss.save('static/uploads/documents/'+director_doc_name, director_doc)
    except:
        director_doc_name = old_director_doc

    User.objects.filter(id=user_id).update(terms=terms,business_doc=business_doc_name,director_doc=director_doc_name,updated_at=datetime.utcnow())

    return HttpResponse(1)
def ptassociation(request):
    user_id = request.session['user_id']
    data = request.POST
    print('data',data)
    disassociate=data['disassociate_id']
    request = Request(
        user_id=user_id,
        invited_user_id=disassociate,
        type='disassociate',
        status=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    request.save()
    return HttpResponse(1)

