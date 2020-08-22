from django.shortcuts import render
from django.http import HttpResponse
from .tasks import sleepy
# Create your views here.

def xmlapp(request):
    sleepy.delay(10)
    return HttpResponse('Done!')