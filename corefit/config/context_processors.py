from django.conf import settings # import the settings file
import numpy as np

def constant(request):
    # return the value you want as a dictionnary. you may add multiple values in there.

    # for i in range(6):
        
    quarterHours = ["00", "15", "30", "45"]
    times = []
    val = ''
    for i in range(12):
        h = 'Hour'
        if i > 1:
            h = 'Hours'
        for j in range(4):
            if i == 0:
                if j > 0:
                    val = str(quarterHours[j])+' Minutes'
                    times.append(val)
            else:
                if j > 0:
                    val = str(i)+" "+h+" "+str(quarterHours[j])+' Minutes'
                    times.append(val)
                else:
                    val = str(i)+" "+h
                    times.append(val)

                if i == 11 and j == 3:
                    val = str(i+1)+" "+h
                    times.append(val)
            
    # json1 = json.list(times)
    # print(json1)

    pt_rating = np.arange(0, 5, 0.5)
    # print(pt_rating)

    context = {
        'LOGO': 'static/images/logo-before-login.png',
        'HTTP_PATH': 'http://127.0.0.1:8000',
        'SITE_TITLE': 'CoreFit',
        'TITLE': 'CoreFit | ',
        'BIO_URL' : "/uploads/bioVideo/",
        'DOCUMENT_URL' : "/uploads/documents/",
        # ******
        'VIRTUAL_TOUR_URL' : "/uploads/virtualTour/",
        'MEDIA_URL' : "/uploads/media/",
        'PROFILE_URL' : "/uploads/profile/",
        # *****
        "CLIENT_TRANSFORMATION_URL":"/uploads/client_media/",
        'user_list' : {
            'Personal Trainer' : 'Personal Trainer',
            'Gym or Studio' : 'Gym or Studio',
            'Sports Coach' : 'Sports Coach',
            'Sports Facility' : 'Sports Facility',
            'Health & Wellness Individual' : 'Health & Wellness Individual',
            'Health & Wellness Company' : 'Health & Wellness Company',
            'Personal Training Company' : 'Personal Training Company',
            'Sports Coaching Company' : 'Sports Coaching Company',
        },
        'training_restriction' : {
            'Male only' : 'Male only',
            'Female only' : 'Female only',
            'Everyone' : 'Everyone',
        },
        'pricing_category' : {
            1 : 'Session',
            2 : 'Services',
            3 : 'Day Pass',
            4 : 'Membership',
            5 : 'Amenity Booking',
        },
        'individual_group' : {    
            'Individual' : 'Individual',        
            'Group' : 'Group',
            
        },
        'currency' : {
            'AED' : 'AED',
            'USD' : 'USD',
            'GBP' : 'GBP',
            'EUR' : 'EUR',
        },
        'booking_length' : times,
        'day_array' : {
            
            1 : 'MON',
            2 : 'TUE',
            3 : 'WED',
            4 : 'THU',
            5 : 'FRI',
            6 : 'SAT',
            7 : 'SUN',
        },
        'promotion_type' : {            
            1 : 'Discount (in terms of percentage)',
            2 : 'Discount (in terms of price reduction)',
            3 : 'Bundle packages with percentage discount',
            4 : 'Bundle packages with price reduction',
            5 : 'Buy X Get Y Free',
        },
        'type_of_services' : {            
            1 : 'Session',
            2 : 'Services',
            3 : 'Day Pass',
            4 : 'Membership',
            5 : 'Videos',
            6 : 'Live Classes',
        },
        'type_of_service' : {            
            1 : 'Session',
            2 : 'Services',
            3 : 'Amenities Booking',
            4 : 'Classes',
            5 : 'Live Classes',
        },
        'pt_rating' : pt_rating,
        'card_type' : {
            'Visa' : 'Visa',
            'MasterCard' : 'MasterCard',
            'American Express' : 'American Express',
            'Discover' : 'Discover',
            'Interlink' : 'Interlink',
            'STAR' : 'STAR',
            'Accel' : 'Accel',
            'Interac' : 'Interac',
            'Visa ReadyLink' : 'Visa ReadyLink',
            'PULSE' : 'PULSE',
            'JCB' : 'JCB',
        },
        'request_status' :  {
            0: 'Pending',
            1: 'Approved',
            2: 'Rejected',
        }
    }
    return context
