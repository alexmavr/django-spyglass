from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils.timezone import now
from django.conf import settings
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
        self.old_authorized_queries = settings.SPYGLASS_AUTHORIZED_QUERIES
        self.old_add_user = settings.SPYGLASS_ADD_USERS

    def tearDown(self):
        settings.SPYGLASS_AUTHORIZED_QUERIES = self.old_authorized_queries
        settings.SPYGLASS_ADD_USERS = self.old_add_user

    # simple GET of receive_query
    def test_GET_index(self):
        resp = self.client.get(reverse('receive_query'))
        self.assertEqual(resp.status_code, 302)

    # Adds a query with the email of the active user
    def test_POST_accept_old_user(self):
        settings.SPYGLASS_AUTHORIZED_QUERIES = False
        settings.SPYGLASS_NEW_USERS = True
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
    # Should create a new user
    def test_POST_accept_new_user(self):
        settings.SPYGLASS_AUTHORIZED_QUERIES = False
        settings.SPYGLASS_NEW_USERS = True
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

    # Adds query with a different email than the user's
    def test_POST_decline_new_user(self):
        settings.SPYGLASS_AUTHORIZED_QUERIES = False
        settings.SPYGLASS_NEW_USERS = False

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
        self.assertGreater(q.next_check, now())
        self.assertGreater(q.next_check, prev_time)


