from django.test import TestCase

from rango.models import Category

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

