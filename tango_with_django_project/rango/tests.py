from django.test import TestCase
from django.urls import reverse

from rango.models import Category

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        """
        When a Category is created we ensure that its view count
        is not negative
        """

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation ensure that when we create a new category
        with capitals and spaces, the slug is all lower case and with
        dashes. In other words, "Random Cat String" -> "random-cat-string"
        """

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

    def test_index_view_with_no_categories(self):
        """
        If no categories exists, the correct message should be displayed.
        """
        # create a client browser object and issue a request for the index page
        # Observe we have to use the namespaced version to pass the test.
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        When categories exists, they are displayed on the index page
        """
        cat_list = ['tpm', 'test', 'temp']
        complex_cat = " ".join(cat_list)
        add_cat(cat_list[0], 1, 1)
        add_cat(cat_list[1], 1, 1)
        add_cat(cat_list[2], 1, 1)
        add_cat(complex_cat, 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        #print(">>> {0}".format(str(response.content)))
        # Avoiding typos!
        self.assertContains(response, complex_cat)

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)
