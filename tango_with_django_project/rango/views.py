import re
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

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
        pages = Page.objects.filter(category=category).order_by('-views')
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

                # Update the date fields. No need for special logic here the model does the hard word for us
                page.first_visit = timezone.now()
                page.last_visit = timezone.now()

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

@login_required
def edit_profile(request, user_profile_id):

    try:
        user = User.objects.get(id=user_profile_id)
    except User.DoesNotExist:
        user = None

    context_dict = {}
    error_dictionaries = {}
    has_error = False

    if user is None:
        error_dictionaries['user_lookup_error'] = 'user id {0} could not be found.'.format(str(user_profile_id))
        print('user id {0} could not be found.'.format(str(user_profile_id)))
        has_error = True

    if user.id != request.user.id:
        error_dictionaries['user_mismatch_error'] = 'user id and request user id are different.'
        print('user id and request user id are different.')
        has_error = True

    user_profile = None

    try:
        if has_error is False:
            user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print('No Profile found for user {0}'.format(str(user.username)))
        has_error = True

    if request.method == 'POST' and has_error is not True:
        # In order to update data we already have,
        #  we need to bind the form object to the instance we retrieved from the back-end!
        # https://stackoverflow.com/questions/26651688/django-integrity-error-unique-constraint-failed-user-profile-user-id#26652053
        form = UserProfileForm(request.POST, request.FILES or None, instance=user_profile)

        # NOTE: to read the value of a check-box it must have a name and a value.
        # When the widget is 'checked' the value set in HTML is passed to this view for processing.
        # Otherwise, (eg no checked) the field is not provided at all. Hence python variable will be None
        clear_image = request.POST.get('clear_image')

        if form.is_valid():
            # TODO: this seems to allow for changing user profiles willyneely
            the_profile = form.save(commit=False)

            if clear_image is not None and  '' != clear_image:
                # SNAG: this does not allow the overload in the Model to delete the underlying file
                # On the plus side, if the user clears the default, it does not delete the default image file!
                the_profile.picture = None

            # This code updates the image correctly, but does not remove the orphaned one.
            # Removal is done in the save overload of the model.
            the_profile.save()
            # Redirects to the user's profile page
            return profile(request, user_profile_id)
        else:
            error_dictionaries['validation_errors'] = form.errors
    else:
        # print('Allowing {0} to edit his/her data.'.format(str(user.username)))
        form = UserProfileForm()

    if has_error:
        return HttpResponseRedirect("/")

    # Something might have gone wrong, but at least messages are directed to the correct user!
    context_dict['form'] = form
    context_dict['user_profile'] = user_profile
    context_dict['error_dictionaries'] = error_dictionaries
    context_dict['has_error'] = has_error
    context_dict['user_profile_id'] = user_profile_id

    return render(request, 'rango/edit_profile.html', context_dict)

@login_required
def like_category(request):
    """
    This function only returns the number of likes for
    a given category. 0 might indicate that the category
    does not exists.

    The result is to be handled in Javascript so that the value
    may be refreshed without apparent page reload.

    IMPORTANT: Disable script blockers!
    """
    category_id = None
    # Figure out which category has been liked.
    if request.method == 'GET':
        # if the category_id keyword present?
        if 'category_id' in request.GET:
            category_id = request.GET['category_id']

    likes = 0

    if category_id:
        category = Category.objects.get(id=category_id)
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()

    response = HttpResponse(likes)
    return response

def get_category_list(max_results=0, starts_with=''):

    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if cat_list and max_results > 0:
        if cat_list.count() > max_results:
                cat_list = cat_list[:max_results]

    return cat_list

def suggest_category(request):

    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    # We re-use the cats.html template but we MUST be sure
    # to label the data correctly!
    # A name mis-match will lead to data not being displayed
    return render(request, 'rango/cats.html', {'cats': cat_list })
