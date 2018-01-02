from django.shortcuts import render
from rango.models import Category

def index(request):
    # Our requirements is to show the top 5 categories.
    # Therefore, we poll of the categories arranged by number
    # of likes and supply the first 5 to our template for display
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'boldmessage': "I am bold font from the context",
                    'categories' : category_list
    }
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context={'message': "About Page!"}
    return render(request, 'rango/about.html', context)