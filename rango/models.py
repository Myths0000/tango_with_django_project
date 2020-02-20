from django.db import models
from email.policy import default
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    
    #primary key (model id, name)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # since slugify() only makes the slugs lower case 
    slug = models.SlugField(unique=True)
    
    # override save() method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # calls the parent save() method to save the changes to correct databse table
        super(Category, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name_plural = 'Categories'
    #changing plural spellings
    
    def __str__(self):
        return self.name
    #useful when debugging or accessing the object in Django shell: <Category: Python>
    #override toString() in Java
    
class Page(models.Model):
    TITLE_MAX_LENGTH =128
    URL_MAX_LENGTH = 200
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # one-to-many relationship, field's constructor
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
        
        
        
        
