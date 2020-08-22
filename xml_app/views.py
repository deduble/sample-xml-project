from django.shortcuts import render
from django.http import HttpResponse
from .tasks import sleepy, sendemailtask, parseXML
# Create your views here.

def xmlapp(request):
    parseXML.delay('default','https://www.w3schools.com/xml/plant_catalog.xml')
    return HttpResponse('Done!')