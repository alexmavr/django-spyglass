from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .views import receive_query
from .views import change_crawlie_access
from .views import admin_panel
from .models import Query
from .models import Crawler
from .models import Site
from tastypie.models import ApiKey

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

# Testcase for the admin panel
class AdminPanelTestcase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Panel is available only to staff
    @override_settings(SPYGLASS_ADMIN_PANEL=True)
    def test_staff_access(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = False
        self.assertRaises(PermissionDenied, admin_panel, request)

    # Panel is available only if the flag is True
    @override_settings(SPYGLASS_ADMIN_PANEL=False)
    def test_setting_flag(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = True
        self.assertRaises(PermissionDenied, admin_panel, request)

    # Normal function scenario
    def test_normal_function(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = True
        response = admin_panel(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("admin_panel.html")



# Testcase for changing crawler api access
class ChangeAccessTestcase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Available only to staff
    def test_staff_access(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = False
        self.assertRaises(PermissionDenied, change_crawlie_access, request, \
                          request.user.id, 1)

    # Consecutive calls of the view with different actions
    def test_create_and_delete(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = True
        key = ApiKey.objects.get(user_id=request.user.id)

        response = change_crawlie_access(request, request.user.id, '1')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("admin_panel.html")
        Crawler.objects.filter(api_key=key.key)

        response = change_crawlie_access(request, request.user.id, '0')
        with self.assertRaises(Crawler.DoesNotExist):
            Crawler.objects.get(api_key=key)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("admin_panel.html")
        newkey = ApiKey.objects.get(user_id=request.user.id)
        self.assertNotEqual(key.key, newkey.key)

    # View should only work for '1' or '0' as action
    def test_invalid_action(self):
        request = self.factory.get(reverse('admin_panel'))
        request.user = create_user()
        request.user.is_staff = True
        with self.assertRaises(Http404):
            change_crawlie_access(request, request.user.id, '4')


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
        response = self.client.get(reverse('receive_query'))
        query = Query.objects.get(params='query text')

        self.assertEqual(response.status_code, 302)

        self.assertEqual(query.user, request.user)
        self.assertEqual(query.params, request.POST['params'])
        self.assertEqual(query.result, None)
        self.assertEqual(query.completed, False)
        self.assertEqual(query.site.pk, 1)

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
        self.assertTemplateUsed(response, 'thanks.html')
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

    # Dont create a query for another user and return 403
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
        self.assertRaises(PermissionDenied, receive_query, request)
        with self.assertRaises(Query.DoesNotExist):
            Query.objects.get(params='not created')

    # SPYGLASS_ADD_USERS=False
    # Dont add new user's query and return 403
    @override_settings(SPYGLASS_ADD_USERS = False)
    def test_decline_nonexistant(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        site = create_site()
        request.POST = { 'params': 'not created',
                        'email': 'other@mail.com',
                        'site': site.pk,
                        'persistent': True }
        with self.assertRaises(PermissionDenied):
            receive_query(request)
        with self.assertRaises(Query.DoesNotExist):
            Query.objects.get(params='not created')

    # SPYGLASS_ADD_USERS=False
    # Dont add new user's query and return 403
    @override_settings(SPYGLASS_ADD_USERS = False)
    def test_decline_unauthorized_nocreate(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        otheruser = create_user(**{'username':'otheruser',
                                 'email':'othermail@mail.com'})
        site = create_site()
        request.POST = { 'params': 'not created',
                        'email': otheruser.email,
                        'site': site.pk,
                        'persistent': True }
        with self.assertRaises(PermissionDenied):
            receive_query(request)
        with self.assertRaises(Query.DoesNotExist):
            Query.objects.get(params='not created')

    # SPYGLASS_ADD_USERS=False
    # Accept a query for the request.user
    @override_settings(SPYGLASS_ADD_USERS = False)
    def test_accept_own_query(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user()
        site = create_site()
        request.POST = { 'params': 'not created',
                        'email': request.user.email,
                        'site': site.pk,
                        'persistent': True }
        receive_query(request)
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
