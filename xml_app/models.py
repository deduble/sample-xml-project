from django.conf import settings
from django.db import models

class FileXML(models.Model):
    name =   models.CharField(max_length=255,blank=True,null=True)
    url =   models.CharField(max_length=255,blank=True,null=True)
    hash =  models.CharField(max_length=255,blank=True,null=True)
    xmlFile = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.name

class Element(models.Model):
    tag             = models.CharField(max_length=100,blank=True,null=True)
    text             = models.CharField(max_length=100,blank=True,null=True)
    tail             = models.CharField(max_length=100,blank=True,null=True)
    mainFile   = models.ForeignKey(FileXML,related_name='file', blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag
    class Meta:
        ordering = ["-tag"]
    @staticmethod
    def get_messages():
        return None
        #return Message.objects.filter(topic__in=topicList__topic).order_by('timestamp')

class Parentship(models.Model):
    currentElement  = models.ForeignKey(Element,null=True,related_name='parent', on_delete=models.CASCADE)
    parentElement   = models.ForeignKey(Element,related_name='current', on_delete=models.CASCADE)
    mainFile   = models.ForeignKey(FileXML,related_name='fileParentship', blank=True,null=True, on_delete=models.CASCADE)
'''
    def __str__(self):
        if self.parentElement:
            return self.currentElement + "is child of" + self.parentElement
        else:
            return self.currentElement + "is the root"
'''
class Attribute(models.Model):
    element     = models.ForeignKey(Element,on_delete=models.CASCADE)
    key   = models.CharField(max_length=100,blank=True,null=True)
    value   = models.CharField(max_length=100,blank=True,null=True)
    mainFile   = models.ForeignKey(FileXML,related_name='fileAttribute',blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return  self.key
