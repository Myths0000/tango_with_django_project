from django.db import models
from email.policy import default

class Catergory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    #primary key (model id, name)
    
    def __str__(self):
        return self.name
    #useful when debugging or accessing the object in Django shell: <Category: Python>
    #override toString() in Java
    
class Page(models.Model):
    category = models.ForeignKey(Catergory, on_delete=models.CASCADE)
    # one-to-many relationship, field's constructor
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
