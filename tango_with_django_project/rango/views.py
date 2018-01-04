import re

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    # Our requirements is to show the top 5 categories.
    # Therefore, we poll of the categories arranged by number
    # of likes and supply the first 5 to our template for display
    category_list = Category.objects.order_by('-likes')[:5]

    # Using the same technique as above, we get the top pages
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'boldmessage': "I am bold font from the context",
                    'categories' : category_list,
                    'pages'      : page_list,
    }

    return render(request, 'rango/index.html', context_dict)

def about(request):
    context={'message': "About Page!"}
    return render(request, 'rango/about.html', context)

def category(request, category_name_slug):
    context_dict = {}
    context_dict['category_name'] = re.sub(r'[-]+', ' ', category_name_slug)

    try:
        # We should be able to find the category from its slug.
        # If not a DoesNotExist exception is raised. 
        category = Category.objects.get(slug=category_name_slug)
        # when the line below is reached, it means the category was found
        context_dict['category_name'] = category.name

        # Now get all the pages for this category
        # Note: in the Page model, the category field is an object reference!
        pages = Page.objects.filter(category=category)
        # Add the results to the context the template has to render
        context_dict['pages'] = pages

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    context_dict['category_name_slug'] = category_name_slug
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    context_dict = {}
    error_dictionaries = {}

    # Are we handling a POST request?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is this a valid form?
        if form.is_valid():
            # save the new category to the database
            form.save(commit=True)

            #retunr the user to the home page
            return index(request)
        else:
            # there are errors. 
            # Capture the HTML code from the form and put it back in a special div
            error_dictionaries['validation_errors'] = form.errors
    else:
        # Request was not a POST, so present a form to enter data into
        form = CategoryForm()

    # Bad form (or form details), no form supplied
    # Render the form with error messages if applicable

    context_dict['form'] = form
    context_dict['error_dictionaries'] = error_dictionaries

    return render(request,'rango/add_category.html', context_dict)

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    
    context_dict = {}
    error_dictionaries = {}

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat 
                page.views = 0
                page.save()
                # Probably better to use a redirect here
                return category(request, category_name_slug)
        else:
            error_dictionaries['validation_errors'] = form.errors
    else:
        # Allow the user to add a page to this category
        form = PageForm()

    context_dict['form'] = form
    context_dict['category'] = cat
    context_dict['error_dictionaries'] = error_dictionaries

    return render(request, 'rango/add_page.html', context_dict)

def register(request):

    # Let's figure out if the user is already known, etc
    registered = False
    context_dict = {}
    error_dictionaries = {}

    # If we are posting, then process the data
    if 'POST' == request.method:
        # Grab the raw data from the request
        # We are processing 2 models in the same request
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if both sets are valid:
        if user_form.is_valid() and profile_form.is_valid():
            # save this into the database
            user = user_form.save()

            # now hash the password using the set password method
            user.set_password(user.password)
            user.save()

            # Now deal with the UserProfile instance.
            # We delay saving the model to avoid integrity issues, hence the commit=False
            profile = profile_form.save(commit=False)
            profile.user = user

            # If a picture is provided place it in the model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now save the instance
            profile.save()

            # Success!
            registered = True
        else:
            # Invalid form data
            error_dictionaries['user_validation_errors'] = user_form.errors 
            error_dictionaries['profile_validation_errors'] = profile_form.errors

    # GET request, show the forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Capture the context
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
    context_dict['error_dictionaries'] = error_dictionaries

    # Render the template
    return render(request, 'rango/register.html', context_dict)

def user_login(request):

    context_dict = {}
    error_dictionaries = {}

    # Handle data submitted through POST method
    if 'POST' == request.method:

        # The username and password
        # Using the GET method will ensure that an exception is raised.
        # Using another method will return "None". This is not what we want
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Leverage Django internals to work out if these are valid credentials
        user = authenticate(username=username, password=password)

        # Instance is valid - the user was found
        if user:
            # is this an active user though?
            if user.is_active:
                # log the user into the application and redirect to the index
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                error_dictionaries['disabled_account'] = 'Your Rango account is disabled'

        else:
            # Invalid credentials, cannot log the user in
            print("Invalid login details for user {0} with password {1}.".format(str(username), str(password)))
            error_dictionaries['invalid_account'] = 'Invalid login details supplied'

    # This is a GET request
    else:
        # Present the form. No context data needed
        pass
    
    # Prepare to display the page
    
    context_dict['error_dictionaries'] = error_dictionaries

    return render(request, 'rango/login.html', context_dict)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!<br /><a href=\"/rango/logout/\">Log out?</a>")

# This decorator ensures that only valid users can accept this view
@login_required
def user_logout(request):
    # we are confident the user is logged in. Log them out ow
    logout(request)
    return HttpResponseRedirect('/rango/')