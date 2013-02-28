from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.auth.models import AnonymousUser
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

    # simple GET of receive_query
    def test_GET_index(self):
        resp = self.client.get(reverse('receive_query'))
        self.assertEqual(resp.status_code, 302)

    # Create a query from the current user
    def test_accept_old_user(self):
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

    # SPYGLASS_ADD_USERS=True
    # Create a query with a new user as another user
    @override_settings(SPYGLASS_ADD_USERS = True)
    def test_user_creation_as_existing(self):
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

    # SPYGLASS_ADD_USERS=True
    # SPYGLASS_AUTHORIZED_QUERIES=False
    # Create a query with a new user as AnonymousUser
    @override_settings(SPYGLASS_ADD_USERS = True)
    def test_user_creation_as_anonymous(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = AnonymousUser()
        site = create_site()
        request.POST = { 'params':'query text',
                        'email': 'othermail@gmail.com',
                        'site': site.pk,
                        'persistent':True }

        response = receive_query(request)
        self.assertEqual(response.status_code, 302)
        query = Query.objects.get(params='query text')

        self.assertEqual(query.user.email, 'othermail@gmail.com')
        self.assertEqual(query.user.username, 'othermail')
        self.assertEqual(query.params, request.POST['params'])
        self.assertEqual(query.result, None)
        self.assertEqual(query.completed, False)
        self.assertEqual(query.site.pk, site.pk)
        self.assertGreater(now(), query.last_mod)

    # Dont create a query for another user and return 401
    def test_decline_unauthorized(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        site = create_site()
        otheruser = create_user(**{'username':'otheruser',
                                 'email':'othermail@mail.com'})
        request.POST = { 'params': 'not created',
                        'email': otheruser.email,
                        'site': site.pk,
                        'persistent': True }
        response = receive_query(request)
        self.assertEqual(response.status_code, 401)
        with self.assertRaises(Query.DoesNotExist):
            Query.objects.get(params='not created')

    # SPYGLASS_ADD_USERS=False
    # Dont add new user's query and return 401
    @override_settings(SPYGLASS_ADD_USERS = False)
    def test_decline_nonexistant(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        site = create_site()
        request.POST = { 'params': 'not created',
                        'email': 'other@mail.com',
                        'site': site.pk,
                        'persistent': True }
        response = receive_query(request)
        self.assertEqual(response.status_code, 401)
        with self.assertRaises(Query.DoesNotExist):
            Query.objects.get(params='not created')

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

