
from django.contrib.auth.models import User
from django.db import models

class Directory(models.Model):
    name = models.CharField(max_length=256) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('Directory', null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    path = models.CharField(max_length=4096, default='')

class File(models.Model):
    SH1a = models.CharField(primary_key=True,max_length=40)
    name = models.CharField(max_length=256)
    ext = models.CharField(max_length=10)
    size = models.IntegerField(default=0)
    directory= models.ManyToManyField(Directory,related_name='files')
    links = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

class Exif(models.Model):
    photo = models.OneToOneField(File, on_delete=models.CASCADE)
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    lens = models.CharField(null=True,max_length=50)
    camera = models.CharField(null=True,max_length=50)
    shoot_time = models.DateTimeField(null=True)
    iso = models.CharField(null=True,max_length=5)
    exposuretime = models.CharField(null=True,max_length=10)
    focallength = models.CharField(null=True,max_length=5)
    
class Mpeg(models.Model):
    mpeg = models.OneToOneField(File, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    video = models.CharField(null=True,max_length=50)
    audio = models.CharField(null=True,max_length=50)
    create_time = models.DateTimeField(null=True)
    

    
