# Tango with Rango

## Introduction

This GIT repository is my active learning trail for the Django tutorial "Tango with Rango". As I write these lines, this is the most complete tutorial I have found on this framework. I wish to solidify the learning I have done so far via sites such as Pluralsight. Along with this, I want to be able to build a planning utility for Alexandra and myself
soon.

## Aims

1. Leverage Python virtual environment (virtualenv).
2. Improve confidence in working with Web Applications.

## HTML-Boilerplate envy

Today, I have wasted a lot of time looking into the [HTML5 Boilerplate project](https://github.com/h5bp/html5-boilerplate). Indeed, there should be little need for me to handcraft all of the required CSS code for this learning application. Likewise, I would like to learn how to leverage such a framework. I write these lines to acknowledge that I wanted to chew too much too soon. Now is not the time to refactor the code to include this framework.

I may have identified, however, a Django Project that could make this process easier ([Github link](https://github.com/mattsnider/django-html5-boilerplate)). Truthfully, I cannot commit myself to believe that this project, which has not been touched in 5 years, can provide the latest version of the project. If it is great! because, it is compatible with `pip` meaning that I will not have to track this as part of any repository.

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

### Using VirtualEnv Wrapper for Windows

This is certainly the highlight of this chapter. I was too eager to use the virutalenv command like I have seen in the Pluralsight courses. The wrapper is much more powerful. Especially since the various packages are now downloaded within the subdirectory of the local repositories but rather outside in the user current profile. That means that I have been able to remove the ``venv`` folder from the local directory. Likewise, I can now call the command ``workon rango`` and it should set me
up directly into the correct GIT repo. Because I already had installed various packages I add to redo that as follows:

``
pip install -r requirements.txt
``

Python apparently installed everything from the cache this time around. Accordingly, I have decided to reset the `gitignore` file.

### Chapter 04

This was a punishing chapter. Indeed, the linking of a the very simple view turned into a major debuging exercise. This is because we have the latest and greatest verison of Django installed and, by contrast, the tutorial refers to an old version of it. Going forward, we have the choice of going back to an old version of Django and refactor the code, or pay attention! For now, I have decided to keep with Django 2.0.

#### Chapter 09

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

   Lionel Saliou, Ph.D
