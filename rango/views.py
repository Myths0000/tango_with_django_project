from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
    form = CategoryForm()
    
    # check if the HTTP request was a POST (did the user submit data via the form)
    # when submitting the contents of a HTML form
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            #cat = form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect(reverse('rango:index'))
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
            
        else:
            print(form.errors)

    # passes the category object through to the template
    context_dict = {'form': form, 'category': category} 
    return render(request, 'rango/add_page.html', context=context_dict)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        