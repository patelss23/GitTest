import os
from string import join
from PIL import Image as PImage
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from photo_share.settings import MEDIA_ROOT
from tempfile import NamedTemporaryFile
from django.core.files import File
from os.path import join as pjoin

class Album(models.Model):
    title = models.CharField(max_length=60)
    pulbic = models.BooleanField(default=False)

    def images(self):
        lst = [(x.title,x.image.name) for x in self.image_set.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x[1],x[1].split('/')[-1]) for x in lst]
        return join(lst,',')
    images.allow_tags = True
    
    def __unicode__(self):
        return self.title
    
class Tag(models.Model):
    tag = models.CharField(max_length=60)
    def __unicode__(self):
        return self.tag
    
class Image(models.Model):
    title = models.CharField(max_length=60,blank=True,null=True)
    image = models.ImageField(upload_to="images/")
    tags = models.ManyToManyField(Tag,blank=True)
    albums = models.ManyToManyField(Album,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    user = models.ForeignKey(User,null=True,blank=True)
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)

    def save(self,*args,**kwargs):
        """save image dimentions"""
        print "save",args,kwargs
        super(Image,self).save(*args,**kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT,self.image.name))
        self.width,self.height = im.size

        # large thumbnail
        fn,ext = os.path.splitext(self.image.name)
        im.thumbnail((128,128),PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name,"BMP")
        self.thumbnail2.save(thumb_fn,File(open(tf2.name)),save=False)
        tf2.close()

        super(Image,self).save(*args,**kwargs)
        
    def size(self):
        return "%s x %s" % (self.width,self.height)
    
    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        #print lst   
        return str(join(lst,','))
    
    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst,','))
    
    
    def thumbnail(self):
        #print """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (self.image.name,self.image.name)
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (self.image.name,self.image.name)
    thumbnail.allow_tags = True
    
    def __unicode__(self):
        return self.image.name
    
class AlbumAdmin (admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title","images"]
    
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "rating","size","tags_","albums_","thumbnail","created"]
    list_filter = ["tags","albums","user"]
    
    def save_model(self,request,obj,form,change):
        print "save_model:",obj,type(obj)
        obj.user = request.user
        obj.save()
    
admin.site.register(Album,AlbumAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Image,ImageAdmin)
