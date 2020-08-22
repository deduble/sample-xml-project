from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from time import sleep
import requests
import xml.etree.ElementTree as ET
from django.core.files.base import ContentFile
from celery.signals import worker_ready
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
def parseXML(email,name, url):
    r = requests.get(url, allow_redirects=True)
    root = ""
    try:
        root = ET.fromstring(r.text)
    except:
        print("exiting...")
        send_mail('Error in Parsing XML File',
        'There is an error occured while parsing your XML file',
        'onuraydin@fastmail.com',
        [email],
        fail_silently=False)
        return None
    hash_object = hashlib.md5(r.text.encode())
    md5_hash = hash_object.hexdigest()
    newXML = FileXML(name=name,url=url,hash=md5_hash)
    newXML.xmlFile.save(name,ContentFile(r.text))
    newXML.save()
    if root:
            helperParseXML(newXML,None,root)
    return None

@worker_ready.connect
def checkExistingFiles(sender,**kwargs):
    allFiles = FileXML.objects.all()
    for fil in allFiles:
        r = requests.get(fil.url, allow_redirects=True)
        hash_object = hashlib.md5(r.text.encode())
        md5_hash = hash_object.hexdigest()
        if md5_hash == fil.hash:
            newXML = FileXML(name=fil.name,url=fil.url,hash=md5_hash)
            newXML.xmlFile.save(fil.name,ContentFile(r.text))
            newXML.save()
            root = ""
            root = ET.fromstring(r.text)
            if root:
                    helperParseXML(newXML,None,root)



@shared_task
def changeText(email, fileid, oldText, newText):
    mafile = FileXML.objects.filter(id=fileid)
    elements = Element.objects.filter(mainFile=mafile[0])
    repCount = 0
    eleCount = 0

    for el in elements:
        count = el.text.count(oldText)
        el.text = el.text.replace(oldText, newText, count)
        if count != 0:
            el.save()
            eleCount += 1
            repCount += count
    send_mail('XML Edit Results',
            'The word: ' + str(oldText) + ' changed with the word: ' + str(newText) + ', ' + str(repCount) + ' times. The count of affected elements is ' + str(eleCount),
            'onuraydin@fastmail.com',
            [email])
    #print('The word: ' + str(oldText) + ' changed with the word: ' + str(newText) + ', ' + str(repCount) + ' times. The count of affected elements is ' + str(eleCount))
    #print(eleCount)

