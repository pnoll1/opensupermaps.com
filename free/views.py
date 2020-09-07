from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
import datetime
import os
import re
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

