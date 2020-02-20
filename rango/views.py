from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime

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
    
    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    
    #return HttpResponse("Rango says hey there partner!" + "<a href='/rango/about/'>About</a>")
    #context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    #request.session.set_test_cookie()
    return render(request, 'rango/index.html', context=context_dict)
    #visitor_cookie_handler(request, response)
    #return response
         
def about(request):
    #return HttpResponse("HttpResponse: 'Rango says here is the about page.'" + "<a href='/rango/'>Index</a>")
    """if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    """
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    return render(request, 'rango/about.html', context=context_dict)

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

@login_required
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

@login_required
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
        
def register(request):
    registered =False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database!!
            user = user_form.save()
            
            # hash the password with the set_password method
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
    
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, render our form using two ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()       
        
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'rango/register.html', context=context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's machinery will check if the username/password combination is valid
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # 
        return render(request, 'rango/login.html')
        
        
@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    context_dict = {}
    context_dict['message']="Since you're logged in, you can see this text!"
    return render(request, 'rango/restricted.html', context=context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

# helper method
# server-side data instead of client-base
# user/session data is stored server-side
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# session ID cookie is still used to remember the client's machine 
# it is just a helper function and does not return a response object
def visitor_cookie_handler(request):
    # default to be 1 if not 
    #visits = int(request.COOKIES.get('visit', '1'))
    #last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))

    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #response.set_cookies('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        #response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie
        
    #response.set_cookie('visits', visits)
    request.session['visits'] = visits
    
    
    
    