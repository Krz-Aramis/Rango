# Tango with Rango

## Introduction

This GIT repository is my active learning trail for the Django tutorial "[Tango with Django](http://www.tangowithdjango.com/book17/chapters/tango.html)". As I write these lines, this is the most complete tutorial I have found on this framework. I wish to solidify the learning I have done so far via sites such as Pluralsight. Along with this, I want to be able to build a planning utility for Alexandra and myself
soon.

## I am bad at CSS

I have spent of lot of time... in fact too much time today, trying to fix this or that in Rango. A lot of time, it was because some elements are not displayed the way I want them to be. The most enraging things are when a good example is found online, but even copy and pasting does not give the expected results. I am especially worried when some designers have solved the "CSS problem" using Javascript. Still, there are tons of elements within Rango that could use the "eye" of a designer. This is not me. I should continue to focus on providing the functionality. After all, this is what a Django application does. The layout and playing or learning about CSS can come at a later point. Actually, it might be better as applying CSS skills will have a material impact on something I have already built.

## HTML-Boilerplate envy

Today, I have wasted a lot of time looking into the [HTML5 Boilerplate project](https://github.com/h5bp/html5-boilerplate). Indeed, there should be little need for me to handcraft all of the required CSS code for this learning application. Likewise, I would like to learn how to leverage such a framework. I write these lines to acknowledge that I wanted to chew too much too soon. Now is not the time to refactor the code to include this framework.

I may have identified, however, a Django Project that could make this process easier ([Github link](https://github.com/mattsnider/django-html5-boilerplate)). Truthfully, I cannot commit myself to believe that this project, which has not been touched in 5 years, can provide the latest version of the project. If it is great! because, it is compatible with `pip` meaning that I will not have to track this as part of any repository.

## Decoupling settings and code

Through this tutorial, there are mentions that some of the approaches we are taking are acceptable in local development, however might pose a risk during deployment. Needless to say, more experienced Django developers are very aware of this and therefore there are efforts to decouple the application from its configuration, such as with the [python decouple project](https://pypi.python.org/pypi/python-decouple). As with the above, it is compatible with `pip` and therefore we should not need to maintain it in GIT.

## Assumptions

- We will use the latest version of Python and Django for this tutorial. This is despite the fact that the book references old versions of both.

## Live Journal

### Chapter 2

I have read the 2nd [chapter](http://www.tangowithdjango.com/book17/chapters/overview.html "Overview" ) in full.

I have installed the latest version of Python for Windows and I can find in the the path.

Using `pip`, I installed the `virtualenv` package.

__Remember__! To create an environment named *venv* use the command:

``virtualenv venv``

This will create a `venv` directory within the current directory. To activate the enviroment, use the command ``venv\Scripts\activate``. This will change the command line prompt.

__Installation Error__: I downloaded the first package offered from the official Website. Sadly, it is the 32-bit installer. I give up for now, but next time, I will make sure to use the 64-bit version.

DJANGO installed within the virutal enviroment. Here is an extract from ``pip freeze``:

``
Django==2.0
pytz==2017.3
``

### Chapter 3

#### Using VirtualEnv Wrapper for Windows

This is certainly the highlight of this chapter. I was too eager to use the virutalenv command like I have seen in the Pluralsight courses. The wrapper is much more powerful. Especially since the various packages are now downloaded within the subdirectory of the local repositories but rather outside in the user current profile. That means that I have been able to remove the ``venv`` folder from the local directory. Likewise, I can now call the command ``workon rango`` and it should set me
up directly into the correct GIT repo. Because I already had installed various packages I add to redo that as follows:

``
pip install -r requirements.txt
``

Python apparently installed everything from the cache this time around. Accordingly, I have decided to reset the `gitignore` file.

### Chapter 04

This was a punishing chapter. Indeed, the linking of a the very simple view turned into a major debuging exercise. This is because we have the latest and greatest verison of Django installed and, by contrast, the tutorial refers to an old version of it. Going forward, we have the choice of going back to an old version of Django and refactor the code, or pay attention! For now, I have decided to keep with Django 2.0.

### Chapter 09

Here is an idea to *deal with possible view errors*:

- In the `base.html`, test for the `error_dictionaries` variables.
- In all of the views, when errors are encountered, append all the required dictionaries under the above.
- In the `base.html`, iterate throught the dictionaries such as follows:

``
{% if error_dictionaries %}
    {% for error in error_dictionaries $}
        {% for data in error_dictionaries[error] $}
            <div class="fail">
                {{ data }}
            </div>
        {$ endfor %}
    {$ endfor %}
{% endif %}
``

Ideally, we will have an elegant way to attach the relevant dictionaries to the render's context inside of the `views.py` file, such as convience function:

``
MyClass.AttachErrorDictionaries(context_dict, (aform.error, bform.error))
``

That being said, modifying an input variable in Python does not seem to be the best way to do things. Along with this, this new function will have to be compatible with one or many input dictionaries. This makes the code complex for most views as these only deal with errors from one form. Perhaps, it is best to keep with the current verbose way to deal with this situation and only spend the time to produce a clever "_handler_" if more instances of multiple forms arise.

### No Chapter 15

Although I do have a Microsoft Live Account I will not be signing up for an Azure contract just to do this chapter. First of all, the latest version of the this tutorial does not use Microsoft Azure anymore. Second of all, Microsoft has a weird offer today and requires the signing of a contract. It may not cost me anything, but it looks like more bother than it is worth. I am nearning the end of the tutorial anyways. Should I have the need to truly learn about external service integration, I will revisit this chapter.

## Conclusion

As I write these lines, I have completed the tutorial except for the following items:

- Integrated Bing Search: this was required for one of the last exercise. It might be worth going back to eventually as the final integration required us to re-map the search results to the data layout in our models and leverage AJAX for quickly adding the page to a given category.
- Deploying project on PythonAnyWhere: the CodeSchool guys use Heroku and since Heroku can use GitHub on which I am now subscribe, I will revisit that when I need to learn how to deploy my own application.

I need to follow-up on the above eventually because I decided to skip them. However it is worth highlighting some of the short-comings of the work so far:

- CSS: as stated above. There are visual elements that do not work well in the current verison of the application. Hopefully, getting better at CSS will allow me to fix that.
- Security: My Firefox installation was not complete with security tools this time around (except for script blocking), thus I did not explore if there were obvious security gaps, such as the ability, through request re-write, to edit someone else's profile.
- Registration Form error handling: in one of the recent commit, an area to display errors the _djang-bootstrap4_ way was added. However, the code as it stands does not take advantage of this HTML area. Along with this, the forms managed by the Registration namespace do not display ANY errors (even in the console). This needs to be investigated. It could be that problems arise when using external Django applications, so managing errors and messaging could be a valuable skill.

   Lionel Saliou, Ph.D
