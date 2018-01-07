import re
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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
