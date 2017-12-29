from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world!<br/><br/> <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse("Rango says hey the about page! <br/><br/> <a href='/rango'>Index</a>")