from django.http import HttpResponseRedirect
from django.shortcuts import render
from .. models import *
from django.contrib.auth.hashers import *
import random
import string
from jinja2 import Environment, FileSystemLoader
from django.shortcuts import render
import os
from ..controller.userViews import userType
from django.contrib import messages
from django.conf import settings

# Create your views here.


env = Environment(
    loader=FileSystemLoader('%s/../templates/emails/' % os.path.dirname(__file__)))

def rand_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(15))

def index(request):
    title = 'Index'
    
    context = {
        # 'users': user,
        'pageTitle': title
    }
    return render(request, 'users/index.html', context)

def profile(request):
    title = settings.SITE_TITLE + ' | ' + 'PT-Employee Profile'


    request.session['user_type'] = "Personal Trainer"
    user_id = request.session['user_id']
    userTypes =userType(user_id,request.session['user_type'])
    # print('userTypes',userTypes['user_type1'])
    if userTypes['user_type1'] != request.session['user_type'] and  userTypes['user_type1'] != 'FreelanceTrainer':
        request.session['user_type'] = userTypes['type']
        messages.error(
                    request, f"Your are not allowed for this url .")
        return HttpResponseRedirect('login')

    # print(user_id)
    user = User.objects
    auth = user.get(id=user_id)
    
    amenities = Amenity.objects.all().values_list('id','name').order_by('name')
    equipments = Equipment.objects.all().values_list('id','name').order_by('name')
    services = Service.objects.all().values_list('id','name').order_by('name')
    countries = Country.objects.all().values_list('id','name').order_by('name')
    languages = Language.objects.all().values_list('id','name').order_by('name')
    branchRecords = Branch.objects.all().values_list('id','branch_name').order_by('branch_name')
    
    basicinfo = ''
    awardInfo = ameniinfo = amenityinfo = ''
    equipinfo = equipmentinfo = ''
    basicinfo2=''
    if BasicInfo.objects.filter(user_id=user_id):
        basicinfo2 = BasicInfo.objects.get(user_id=user_id)
    print('id+++',user_id)
    user = User.objects.get(freelance_id=user_id)
    user_id = user.id
    if BasicInfo.objects.filter(user_id=user_id):
        basicinfo = BasicInfo.objects.get(user_id=user_id)
        amenityinfo = UserAmenity.objects.all().filter(user_id=user_id).values()
        ameniinfo = UserAmenity.objects.filter(user_id=user_id)
        equipinfo = UserEquipment.objects.filter(user_id=user_id)
        equipmentinfo = UserEquipment.objects.all().filter(user_id=user_id).values()
        


    amen_arr = []
    if amenityinfo:
        for amm in amenityinfo:
            amen_arr.append(amm['amenity_id'])

    equi_arr = []
    if equipmentinfo:
        for eqmm in equipmentinfo:
            equi_arr.append(eqmm['equipment_id'])

    cities = []

    if basicinfo:
        cities = City.objects.filter(country_id=basicinfo.country).values_list('id','name').order_by('name')




    awardInfo = UserAward.objects.all().filter(user_id=user_id).values()

    # *******
    mediaSocialMedia = UserMediaRecord.objects.all().filter(user_id=user_id, type="myMedia[]").values()

    mediavirtual_tour = UserMediaRecord.objects.all().filter(user_id=user_id, type="virtual_tour").values()
    mediatile_image = UserMediaRecord.objects.all().filter(user_id=user_id, type="tile_image").values()

    mediamyMedia = UserMediaRecord.objects.all().filter(user_id=user_id, type="myMedia[]").values().order_by(
        '-created_at')
    mediaprofile_photo = UserMediaRecord.objects.filter(user_id=user_id, type='ProfilePhoto').values()
    try:

        request.session['pt_profile'] = mediaprofile_photo[0]['data']
    except:
        request.session['pt_profile']=''

    userClientTransformationData = UserClientTransformation.objects.all().filter(user_id=user_id).values()

    if mediamyMedia:
        mediamyMedia = mediamyMedia[0]

    # **********

    urlLink = User.objects.get(freelance_id=auth.id)

    sesstionTypes = Session.objects.all().values_list('id', 'name').order_by('name')
    serviceAmenityTypes = ServiceAmenity.objects.all().values_list('id', 'name').order_by('name')
    amenityTypes = BookableAmenity.objects.all().values_list('id', 'name').order_by('name')
    sports = Sport.objects.all().values_list('id', 'name').order_by('name')
    priceList = UserPrice.objects.filter(user_id=user_id).values()

    existingFaq = ExistingFaq.objects.all().filter().values()
    faq_tabless = UserFaq.objects.all().filter(user_id=user_id).values()

    requestData = []    
    if bool(Request.objects.filter(freelancer_user_id=auth.id,status=1)):
        requestVal = Request.objects.filter(freelancer_user_id=auth.id,status=1).values('type','association_id').first()
        print(requestVal)
        if requestVal['type'] == 'Association':
            BranchData = Branch.objects.filter(id=requestVal['association_id']).values('branch_name').first()
            infoData = BasicInfo.objects.filter(branch_id=requestVal['association_id']).values('location').first()
            
            requestData.append(BranchData['branch_name'])
            requestData.append(infoData['location'])

    # print(cities)
    context = {
        # 'users': user,
        'pageTitle': title,
        'user': auth,
        'facility_types': settings.FACILITY_TYPE,
        'branchRecords': branchRecords,
        'basicinfo': basicinfo,
        'basicinfo2': basicinfo2,
        'languages': languages,
        'countries': countries,
        'cities': cities,
        'services': services,
        'amenities': amenities,
        'equipments': equipments,
        'amenityinfo': amenityinfo,
        'ameniinfo': ameniinfo,
        'equipinfo': equipinfo,
        'equipmentinfo': equipmentinfo,
        'amenityList': amen_arr,
        'equipList': equi_arr,
        'awardList': awardInfo,
        'sesstionTypes': sesstionTypes,
        'serviceAmenityTypes': serviceAmenityTypes,
        'amenityTypes': amenityTypes,
        'sports': sports,
        'priceList': priceList,
        'urlLink': urlLink,

        # *********
        'mediaSocialMedia':mediaSocialMedia,
        'mediavirtual_tour':mediavirtual_tour,
        'mediatile_image':mediatile_image,
        'mediaprofile_photo':mediaprofile_photo,
        'mediamyMedia':mediamyMedia,
        "userClientTransformationData":userClientTransformationData,
        "existingFaq":existingFaq,
        "faq_tabless":faq_tabless,
        "requestData":requestData,
        # **********
    }
   
    return render(request, 'ptTemplates/users/profile.html', context)


def overwritesection(request):
    return render(request, 'ptTemplates/users/overwrite_section.html')

def newOffer(request):
    title = settings.SITE_TITLE + ' | ' + 'New Offer'

    user_id = request.session['user_id']
    offerRecords = UserOffer.objects.filter(user_id=user_id).values()
    serviceRecords = UserPrice.objects.filter(user_id=user_id).values()

    session_records = UserPrice.objects.filter(session_category=1,user_id=user_id).values_list('id','session_name').order_by('session_name')
    service_records = UserPrice.objects.filter(session_category=2,user_id=user_id).values_list('id','session_name').order_by('session_name')
    day_records = UserPrice.objects.filter(session_category=3,user_id=user_id).values_list('id','session_name').order_by('session_name')
    membership_records = UserPrice.objects.filter(session_category=4,user_id=user_id).values_list('id','session_name').order_by('session_name')

    context = {
        'pageTitle': title,
        'offerRecords': offerRecords,
        'serviceRecords': serviceRecords,
        'session_records': session_records,
        'service_records': service_records,
        'day_records': day_records,
        'membership_records': membership_records,
    }

    return render(request, 'ptTemplates/users/new_offer.html', context)



