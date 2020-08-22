from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import requests
import xml.etree.ElementTree as ET
@shared_task
def sleepy(duration):
    sleep(duration)
    print("wake up!")
    return None

@shared_task
def sendemailtask():
    send_mail('Celery Task Worked',
    'this is some content',
    'onuraydin@fastmail.com',
    ['yayawe3291@delotti.com'])
    return None

@shared_task
def parseXML(url):
    r = requests.get(url, allow_redirects=True)
    root = ET.fromstring(r.text)
    #myroot = tree.getroot()
    print(root.tag)
    return None
