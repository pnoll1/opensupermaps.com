from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
#from blog.secret_stuff import endpoint_secret, avalara_user, avalara_key
import datetime
import os
#import stripe
import re
#from avalara import AvataxClient
import json
from operator import itemgetter
from pathlib import Path

# timezone class
class Utc(datetime.tzinfo):
    _offset = datetime.timedelta(hours=0)
    _dst = datetime.timedelta(0)
    def utcoffset(self,dt):
        return self.__class__._offset
    def dst(self, dt):
        return self.__class__._dst

utc = Utc()
def list_map_files(directory):
    '''
    input directory path as string
    output alphabetized lists of map files with each file is list of name, modified time and size
    '''
    files_obf = []
    files_mwm = []
    for file in Path(directory).iterdir():
        modified_time = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime('%m-%d-%y')
        size = round(file.stat().st_size / 1048576, 1)
        name = file.name
        if file.suffix == '.obf':
            files_obf.append([name, modified_time, size])
        if file.suffix == '.mwm':
            files_mwm.append([name, modified_time, size])
    files_obf.sort(key=itemgetter(0))
    files_mwm.sort(key=itemgetter(0))
    return files_obf, files_mwm

def downloads(request):
    context = {}
    context['static'] = '/static'
    files_obf, files_mwm = list_map_files('./free/static/downloads')
    context['files_obf'] = files_obf
    context['files_mwm'] = files_mwm
    # check if user logged in
    #if not request.user.is_authenticated:
    #    return redirect('/downloads-ad')
    # check for valid subscription
    #try:
    #    s = subscriptionFix.objects.get(user=request.user.username)
    #except Exception as e:
    #    messages.error(request, 'Need valid subscription')
    #    return redirect('/downloads-ad')
    # reject expired subscription
    #if request.user.is_authenticated and datetime.datetime.now(utc) < s.end_date:
    #    messages.error(request, 'Need valid subscription')
    return render(request, 'downloads.html', context)
    #else:
    #return redirect('/downloads-ad')

def contact(request): 
    context = {} 
    context['static'] = '/static' 
    return render(request, 'contact.html', context)


def faq(request): 
    context = {} 
    context['static'] = '/static' 
    return render(request, 'faq.html', context)

'''
def downloads_ad(request):
    context = {}
    context['static'] = '/static'
    files_obf, files_mwm = list_map_files('./free/static/downloads')
    context['files_obf'] = files_obf
    context['files_mwm'] = files_mwm
    return render(request, 'downloads_ad.html', context)

def serve_downloads(request):
    context = {}
    context['static'] = '/static'
    if request.user.is_authenticated:
        s = subscriptionFix.objects.get(user=request.user.username)
        if s.end_date > datetime.datetime.now(utc):
            file_name = request.path.split('/')[-1]
            file_path = os.path.join('downloads/static/downloads/' + file_name)
            return FileResponse(open(file_path, 'rb'))
    else:
        messages.error(request, "Must be logged in with valid subscription")
        return redirect('/login')

def login_view(request):
    context = {}
    context['static'] = '/static'
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    # Successfull login
    if user is not None and request.method == 'POST':
        login(request, user)
        messages.success(request, 'Login Successfull')
        return redirect('/downloads')
    # redirect logged in user
    elif request.user.is_authenticated and request.method == 'GET':
        messages.info(request, "You're already logged in")
        return redirect('/')
    # login not yet tried
    elif request.method == 'GET' and user is None:
        return render(request, 'login.html',context)
    # failed login
    else:
        messages.error(request, 'Login Failed')
        return render(request, 'login.html',context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('/')

def register(request):
    context = {}
    context['static'] = '/static'
    # check if form views be better
    #first_name = request.POST.get('first_name')
    #last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    invite_code = request.POST.get('invite_code')
    if username and email and password and password_confirm:
        if password != password_confirm:
            messages.error(request,"The password fields must match")
            return render(request, 'register.html',context)
        # user registration handling
        user = User(username=username, email=email, password=password)
        try:
            user.full_clean()
        except ValidationError as e:
            messages.error(request,e)
            return render(request, 'register.html',context)
        if not User.objects.filter(username=username):
            User.objects.create_user(username=username, email=email, password=password) #, is_active=False
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, 'Username reserved')
            return redirect('/payment')
        messages.error(request, 'Username taken')
    else:
        messages.error(request, 'Fields missing')
    # send confirmation email
    return render(request, 'register.html',context)

def tax(request):
    if request.user.is_authenticated:
        context = {}
        context['static'] = '/static'
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if request.method == "GET":
            return render(request, 'tax.html', context)
        if request.method == "POST" and address and zip and city and state:
            client = AvataxClient('downloads',
                'ver 1.0',
                'my test machine',
                'production')
            client = client.add_credentials(avalara_user, avalara_key)

            tax_document = {
                 "addresses": {
                    "shipFrom": {
                        "line1": "6914 Meadowdale Beach Rd",
                        "city": "Edmonds",
                        "region": "WA",
                        "country": "US",
                        "postalCode": "98026"
                    },
                    "shipTo": {
                        "line1": address,
                        "city": city,
                        "region": state,
                        "country": "US",
                        "postalCode": zip
                    }
                    },
                'commit': False,
                'companyCode': 'DEFAULT',
                'currencyCode': 'USD',
                'customerCode': 'TEST',
                'date': '2017-04-12',
                'description': 'Yarn',
                'lines': [{'amount': 10,
                }],
                'purchaseOrderNo': '2017-04-12-001',
                'type': 'SalesInvoice'}
            transaction_response = client.create_transaction(tax_document)
            # error handling
            if 499 >= transaction_response.status_code >= 400:
                e = json.loads(transaction_response.content)
                messages.error(request, 'Tax calculation failed. If address is valid, send email patrick@patricknoll.com with details' + e['error']['message'] + e['error']['details'][0]['description'])
            if 599 >= transaction_response.status_code >= 500:
                e = json.loads(transaction_response.content)
                messages.error(request, 'Tax calculation service internal error. Please try again.  If error persits, please email patrick@patricknoll.com with details' + e['error']['message'] + e['error']['details'][0]['description'])
            # transaction_response.status_code
            avatax_response = json.loads(transaction_response.content)
            tax = avatax_response['totalTax']
            t = transaction.objects.create(user=request.user.username, address=address, zip=zip, city=city, state=state, commit=False, date=datetime.datetime.now(utc),tax=round(float(tax),2))
            try:
                t.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                #return(tax_form)
            t.save()
            return redirect('/payment')
        else:
            messages.error(request, 'Fields missing')
            return render(request, 'tax.html', context)

def payment(request):
    context = {}
    context['static'] = '/static'
    if request.user.is_authenticated:
        #t = transaction.objects.get(user=request.user.username)
        price = 1000
        # add and convert tax to stripe format
        #tax = int(t.tax*100)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            client_reference_id= request.user.username,
            billing_address_collection='required',
            line_items=[{
                'name': 'US Maps for OSMAnd',
                'description': "State Maps for OSMAnd with millions of addresses added, You'll receive updates monthly for the next 12 months",
                'amount': price,
                'currency': 'usd',
                'quantity': 1,
                }
            ],
            success_url='http://localhost:8002/downloads?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8002/downloads',
            )
        context['CHECKOUT_SESSION_ID'] = session.id
        return render(request, 'payment.html', context)
    else:
        return redirect('/login')


@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase...
        def handle_checkout_session(session):
            s = subscriptionFix.objects.create(user=session['client_reference_id'], end_date=datetime.datetime.now(utc) + datetime.timedelta(days=365))
            try:
                s.full_clean()
                #t.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return HttpResponse(status=500)
            s.save()
            #t.save()
        handle_checkout_session(session) # doesn't do anything, errors out on download page with user has no subscription

    return HttpResponse(status=200)
'''
