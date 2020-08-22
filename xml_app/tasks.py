from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import requests
import xml.etree.ElementTree as ET
from xml_app.models import (
    Element,
    Parentship,
    Attribute
)
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

def helperParseXML(parent,child):
    #create new element
    newElement = Element(tag=child.tag)
    newElement.tag = child.tag
    newElement.tail = child.tail
    newElement.text = child.text
    newElement.save()
    print("sadasda")
    #create parentship
    if parent != None:
        newParentship = Parentship(currentElement=newElement,parentElement=parent)
        newParentship.save() 
    #create attribute
    if child.attrib:
        newAttribute = Attribute(element=child,key=child.key,value=child.attrib.value)
        newAttribute.save()
    for childOfChild in child:
        helperParseXML(newElement,childOfChild)

@shared_task
def parseXML(url):
    r = requests.get(url, allow_redirects=True)
    root = ET.fromstring(r.text)
    if root:
        helperParseXML(None,root)

    print(root.tag)
    return None
