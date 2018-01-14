from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rango.models import Category, Page

def add_cat(name, views, likes):

    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat_name, title, url, views=0, first_visit=None, last_visit=None):

    cat = add_cat(cat_name, 1, 1)
    p = Page.objects.get_or_create(category=cat, title=title, url=url,first_visit=first_visit, last_visit=last_visit)[0]
    p.save()
    return p


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


    def test_page_allow_for_first_visit_to_be_set(self):
        """
        Verifies that when pages are visited for the first time, the model updates accordingly
        """

        first_visit_yesterday = timezone.now() + timedelta(days=-1)
        page = add_page('test', 'test', 'http://example.com', first_visit=first_visit_yesterday)
        self.assertEqual(page.first_visit is not None, True)
        self.assertEqual( first_visit_yesterday == page.first_visit, True)


    def test_page_allow_for_both_visit_data_to_be_set(self):
        """
        Verifies that when pages are re-visited the 'first time' and last visit time can be defined.
        """

        first_visit_last_week = timezone.now() + timedelta(days=-7)
        last_visit_yesterday = timezone.now() + timedelta(days=-1)
        page = add_page('test', 'test', 'http://example.com', first_visit=first_visit_last_week, last_visit=last_visit_yesterday)
        self.assertEqual(page.first_visit is not None, True)
        self.assertEqual( first_visit_last_week == page.first_visit, True)
        self.assertEqual(page.last_visit is not None, True)
        self.assertEqual( last_visit_yesterday == page.last_visit, True)


    def test_page_allow_for_last_visit_to_be_updated(self):
        """
        Verifies that when pages are re-visited the last_visit time is updated accordingly
        """

        first_visit_last_week = timezone.now() + timedelta(days=-7)
        initial_last_visit = timezone.now() + timedelta(days=-2)
        last_visit_yesterday = timezone.now() + timedelta(days=-1)
        page = add_page('test', 'test', 'http://example.com', first_visit=first_visit_last_week, last_visit=initial_last_visit)
        page.last_visit = last_visit_yesterday
        page.save()
        self.assertEqual( last_visit_yesterday == page.last_visit, True)


    def test_page_first_visit_cannot_be_in_the_future(self):
        """
        When pages are added, their first visit information cannot be in the future
        """

        future_first_visit = timezone.now() + timedelta(days=30)
        page = add_page('test', 'test', 'http://test.net', first_visit=future_first_visit)
        self.assertEqual( page.first_visit is not None, True)
        # NOTE: we are not following best practice for testing with time here!
        # therefore, if the test takes time to execute, we tolerate a 10 second
        # gap between 'now' and the moment the page executed its save function
        self.assertEqual( (timezone.now() - page.first_visit).seconds <= 10, True )


    def test_page_first_visit_cannot_be_after_last_visit(self):
        """
        Verifies first visit is never after last visit. If so set both to the earliest date
        """

        earliest_date = timezone.now() + timedelta(days=-7)
        a_date = timezone.now() + timedelta(days=-1)
        page = add_page('test', 'test', 'http://example.com', first_visit=a_date, last_visit=earliest_date)
        self.assertEqual( earliest_date == page.first_visit == page.last_visit, True)


    def test_page_first_visit_cannot_be_updated_once_set(self):
        """
        Verifies that it is not possible to change the first visit date once set
        """

        first_visit_last_week = timezone.now() + timedelta(days=-7)
        last_visit_yesterday = timezone.now() + timedelta(days=-1)
        new_first_visit = timezone.now() + timedelta(seconds=3600)
        page = add_page('test', 'test', 'http://example.com', first_visit=first_visit_last_week, last_visit=last_visit_yesterday)
        page.first_visit = new_first_visit
        page.last_visit = new_first_visit
        page.save()
        self.assertEqual( first_visit_last_week == page.first_visit, True)
        self.assertEqual( new_first_visit == page.last_visit, True)


    def test_page_setting_last_visit_without_first_visit_sets_both(self):
        """
        Verifies that in the case when we set the last visit without records of a first visit,
        the first visit data is also set.
        """

        last_visit_yesterday = timezone.now() + timedelta(days=-1)
        page = add_page('test', 'test', 'http://example.com', last_visit=last_visit_yesterday)
        self.assertEqual( last_visit_yesterday == page.first_visit == page.last_visit, True)


    def test_page_allow_for_both_visit_data_to_be_set_as_the_same_date(self):
        """
        Verifies that when pages are re-visited the 'first time' and last visit time can be defined.
        """

        test_date = timezone.now() + timedelta(days=-7)
        page = add_page('test', 'test', 'http://example.com', first_visit=test_date, last_visit=test_date)
        self.assertEqual(page.first_visit is not None, True)
        self.assertEqual( test_date == page.first_visit, True)
        self.assertEqual(page.last_visit is not None, True)
        self.assertEqual( test_date == page.last_visit, True)
