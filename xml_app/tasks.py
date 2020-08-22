from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import requests
import xml.etree.ElementTree as ET
from django.core.files.base import ContentFile
from xml_app.models import (
    Element,
    Parentship,
    Attribute,
    FileXML
)
import hashlib

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

def helperParseXML(xmlFile, parent,child):
    #create new element
    newElement = Element(tag=child.tag)
    newElement.tag = child.tag
    newElement.tail = child.tail
    newElement.text = child.text
    newElement.mainFile = xmlFile
    newElement.save()
    print("sadasda")
    #create parentship
    if parent != None:
        newParentship = Parentship(currentElement=newElement,parentElement=parent)
        newParentship.mainFile = xmlFile
        newParentship.save() 
    #create attribute
    if child.attrib:
        newAttribute = Attribute(element=child,key=child.key,value=child.attrib.value)
        newAttribute.mainFile = xmlFile
        newAttribute.save()
    for childOfChild in child:
        helperParseXML(xmlFile, newElement,childOfChild)

@shared_task
def parseXML(name, url):
    r = requests.get(url, allow_redirects=True)
    
    hash_object = hashlib.md5(r.text.encode())
    md5_hash = hash_object.hexdigest()
    newXML = FileXML(name=name,url=url,hash=md5_hash)
    newXML.xmlFile.save(name,ContentFile(r.text))
    newXML.save()
    root = ET.fromstring(r.text)
    if root:
        helperParseXML(newXML,None,root)

    print(root.tag)
    return None
