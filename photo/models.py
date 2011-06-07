from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=60)
    pulbic = models.BooleanField(default=False)
    
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
    
    def __unicode__(self):
        return self.image.name
    
class AlbumAdmin (admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]
    
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "rating", "created"]
    list_filter = ["tags","albums"]
    
admin.site.register(Album,AlbumAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Image,ImageAdmin)