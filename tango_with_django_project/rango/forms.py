"""Forms related to the Rango application"""
import re
from django import forms
from django.template.defaultfilters import slugify
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    """The Category Form specifications"""

    name = forms.CharField(max_length=128,
                           help_text="Please enter a category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(),
                               initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),
                               initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),
                           required=False)

    def clean(self):
        """Ensure that we do not end-up with Categories resolving to same slug"""
        cleaned_data = self.cleaned_data
        name_to_lookup = self.cleaned_data['name']

        try:
            test_slug = slugify(name_to_lookup)
            Category.objects.get(slug=test_slug)
        except Category.DoesNotExist:
            return cleaned_data
        raise forms.ValidationError("Non unique Slug!")

    # Inine class to provide additional information on the form
    class Meta:
        """Provides an association between the ModelForm and the model"""

        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    """The Page Form specifications"""

    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")

    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")

    views = forms.IntegerField(widget=forms.HiddenInput(),
                               initial=0)

    def clean(self):
        """Prepends the URL field with http:// if the user does not"""
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if not re.match(r'^http[s]?://', url):
            url = 'http://' + url
            cleaned_data['url'] = url
        
        return cleaned_data

    class Meta:
        """Provide an association between the ModelForm and a model"""
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
