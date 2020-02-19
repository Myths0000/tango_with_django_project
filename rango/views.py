from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # "-" = descending order
    # e.g. [2:10] will return items [2] to [9]
    # [:5] means: retrieve the top 5 only
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
        
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    #return HttpResponse("Rango says hey there partner!" + "<a href='/rango/about/'>About</a>")
    #context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dict)
         
def about(request):
    #return HttpResponse("HttpResponse: 'Rango says here is the about page.'" + "<a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category) # return a list of page objeccts or an empty list
        
        context_dict['pages'] = pages
        context_dict['category'] = category # will be used in the template to verify existence
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context=context_dict)
