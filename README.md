# Tango with Rango

## Introduction

This GIT repository is my active learning trail for the Django tutorial "Tango with Rango". As I write these lines, this is the most complete tutorial I have found on this framework. I wish to solidify the learning I have done so far via sites such as Pluralsight. Along with this, I want to be able to build a planning utility for Alexandra and myself
soon.

## Aims

1. Leverage Python virtual environment (virtualenv).
2. Improve confidence in working with Web Applications.

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

   Lionel Saliou, Ph.D
