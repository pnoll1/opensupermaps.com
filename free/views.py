from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse
from blog.secret_stuff import b2_endpoint, aws_access_key_id, aws_secret_access_key
import datetime
import os
import re
import json
from operator import itemgetter
from pathlib import Path
import boto3

# timezone class
class Utc(datetime.tzinfo):
    _offset = datetime.timedelta(hours=0)
    _dst = datetime.timedelta(0)
    def utcoffset(self,dt):
        return self.__class__._offset
    def dst(self, dt):
        return self.__class__._dst

utc = Utc()

s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,endpoint_url=b2_endpoint)
def list_map_files(directory):
    '''
    input directory path as string
    output alphabetized lists of map files with each file is list of name, modified time and size
    '''
    files_obf = []
    files_mwm = []
    bucket = 'opensupermaps'
    response = s3.list_objects(Bucket=bucket)
    for file in response['Contents']:
        filename = Path(file['Key'])
        if filename.suffix == '.obf':
            url = f'https://{bucket}.s3.us-east-005.backblazeb2.com/{filename}'
            modified_time = file['LastModified'].strftime('%m-%d-%y')
            size = round(file['Size'] / 1048576)
            sha_filename = filename.with_suffix('.sha256')
            sha_url = f'https://{bucket}.s3.us-east-005.backblazeb2.com/{sha_filename}'
            files_obf.append([url, filename.stem.replace('_',' ').upper(), modified_time, size, sha_url, sha_filename.stem.replace('_', ' ').upper()])
    return files_obf

def downloads(request):
    context = {}
    context['static'] = '/static'
    files_obf = list_map_files('static/downloads')
    context['files_obf'] = files_obf
    return render(request, 'downloads.html', context)

def contact(request): 
    context = {} 
    context['static'] = '/static' 
    return render(request, 'contact.html', context)


def faq(request): 
    context = {} 
    context['static'] = '/static' 
    return render(request, 'faq.html', context)

