from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils.timezone import now
from .views import receive_query
from .models import Query
from .models import Site

# Model Factories
def create_user(**kwargs):
    defaults = {
        'username': 'afein',
        'password': 'dummy',
        'email': 'default@gmail.com'
    }
    defaults.update(kwargs)
    return User.objects.create(**defaults)

def create_site(**kwargs):
    defaults = {
        'name': 'dummy site',
        'url': 'http://dummysite.org',
        'poll_time': 10
    }
    defaults.update(kwargs)
    return Site.objects.create(**defaults)


# Testcase for receive_query
class ReceiveQueryViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # GET should just redirect to root
    def test_GET_index(self):
        resp = self.client.get(reverse('receive_query'))
        self.assertEqual(resp.status_code, 302)

    # Adds query with the email of the active user
    def test_POST_old_user(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        request.POST = { 'params':'query text',
                        'email': request.user.email, 'site': 1,
                        'persistent':True }
        response = receive_query(request)
        query = Query.objects.get(params='query text')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(query.user, request.user)
        self.assertEqual(query.params, request.POST['params'])
        self.assertEqual(query.result, None)
        self.assertEqual(query.completed, False)
        self.assertEqual(query.site.pk, 1)

    # Adds query with a different email than the user's
    #   should create a new user with that email
    def test_POST_new_user(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        site = create_site()
        request.POST = { 'params':'query text',
                        'email': 'othermail@gmail.com',
                        'site': site.pk,
                        'persistent':True }
        response = receive_query(request)
        query = Query.objects.get(params='query text')

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(query.user, request.user)
        self.assertEqual(query.user.email, 'othermail@gmail.com')
        self.assertEqual(query.user.username, 'othermail')
        self.assertEqual(query.params, request.POST['params'])
        self.assertEqual(query.result, None)
        self.assertEqual(query.completed, False)
        self.assertEqual(query.site.pk, site.pk)
        self.assertGreater(now(), query.last_mod)

# Testcase for Query model
class QueryModelTestCase(TestCase):
    def test_save(self):
        q = Query.objects.create(user=create_user(),
                                 site=create_site(),
                                 result=None,
                                 completed=False,
                                 persistent=True,
                                 params='save test',
                                 last_mod=now())
        prev_time = q.next_check
        q.save()
        assert q.next_check > now()
        assert q.next_check > prev_time


