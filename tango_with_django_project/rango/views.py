from django.shortcuts import render
from rango.models import Category, Page

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
    
    return render(request, 'rango/category.html', context_dict)