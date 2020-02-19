import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
# important to import django and "MODULE" (crucial steps)
# will get an exception otherwise, because the neccessary Django infrastructure has not been initialized 
django.setup()
from rango.models import Category, Page

def populate():
    # lists of dictionaries of pages
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 1231},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views':926},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views':305}]
    
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views':274},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views':743},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views':454}]
    
    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views':45},
        {'title':'Flask',
         'url':'http://flask.pocoo.org',
         'views':99}]
    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views':32, 'likes':16} }
    
    # Iterate over cats
    # cats.items()
    # cat_data
    for cat, cat_data in cats.items():
        # local variable c will stores a reference to a new category
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
            
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
            
def add_page(cat, title, url, views=0):
        # [0] means only the object reference will be returned
        p = Page.objects.get_or_create(category=cat, title=title)[0]
        p.url = url
        p.views = views
        p.save()
        return p
    
def add_cat(name, views=0, likes=0):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c
        
    # Start execution !!
    # run by using:  python module.py
    # either a standalone or a reusable module like JAVA (class) with optional JAVA (static main):
    # however, code within a conditional if__name__ ... will therefore only be executed
    # when the module is run as a standalone Python script
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()