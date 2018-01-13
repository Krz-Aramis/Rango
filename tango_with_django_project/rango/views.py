import re
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserProfileForm

def index(request):

    rango_index_url = 'rango/index.html'
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

    # Using the Server-side session object, we count number of visits and time of last visit
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False
    # get the handle of the response we are currently building
    response = render(request, rango_index_url, context_dict)

    # Does the key 'last_visit' exist?
    last_visit = request.session.get('last_visit')
    if last_visit:
        # Cast to a valid python date/time object
        # Note: we are discarding the last 7 characters from the string!
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it has been more than a day (.days > 0):
        # For testing 5 seconds will do.
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            # set the flag accordingly so we update the cookie
            reset_last_visit_time = True
    else:
        # cookie does not exist
        reset_last_visit_time = True

    # Update session data
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now() )
        request.session['visits'] = visits

    # Update the visit counter in the request context
    context_dict['visits'] = visits
    response = render(request, rango_index_url, context_dict)

    return response

def about(request):
    context_dict={'message': "About Page!"}

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict['visits'] = count

    return render(request, 'rango/about.html', context_dict)

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

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {'message': "Since you're logged in, you can see this text!"})

def track_url(request):

    page_id = None
    # Figure out which page has been requested.
    if request.method == 'GET':
        # if the page_id keyword present?
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

        # We have an ID, let's look-up the data
        if page_id and page_id is not None:
            try:
                page = Page.objects.get(id=page_id)
                # We have the page!
                # increment the number of views on the this page and save this.about
                views = page.views
                page.views = views + 1
                page.save()
                # Now redirect the user to the requested page
                return HttpResponseRedirect(page.url)
            except Page.DoesNotExist:
                page = None

    # Page ID is bogus or something else went wrong, redirect to the home page
    return HttpResponseRedirect('/')

def register_profile(request):
    registered = False
    context_dict = {}
    error_dictionaries = {}

    if 'POST' == request.method:
        # grab the form data
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            # Using the request object, we work out who we are going the registration for!
            if request.user.is_authenticated:
                profile.user = request.user
            else:
                print("the {0} is not authenticated".format(str(current_user)))

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered=True
        else:
            error_dictionaries['profile_validation_error'] = profile_form.errors
    else:
        profile_form = UserProfileForm()

    if registered:
        # TODO: redirect new users to their profile page.
        return HttpResponseRedirect('/')
    else:
        context_dict['profile_form'] = profile_form
        context_dict['registered'] = registered
        context_dict['error_dictionaries'] = error_dictionaries
        return render(request, 'registration/profile_registration.html', context_dict)

def profile(request, user_profile_id):
    context_dict = {}
    error_dictionaries = {}
    user = None
    user_profile = None

    try:
        user = User.objects.get(id=user_profile_id)

    except User.DoesNotExist:
        error_dictionaries['user_lookup_error'] = 'No such user with id {0}'.format(str(user_profile_id))

    if user is not None:
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            error_dictionaries['user_profile_lookup_error'] = 'No user profile for user {0}'.format(str(user.username))

    context_dict['user_data'] = user
    context_dict['user_profile_data'] = user_profile
    context_dict['error_dictionaries'] = error_dictionaries

    return render(request, 'rango/profile.html', context_dict)

def profiles(request):
    context_dict = {}

    profile_list = UserProfile.objects.all()

    context_dict['profiles'] = profile_list

    return render(request, 'rango/profiles.html', context_dict)
