from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from .views import receive_query
from .models import Query

# Model Factories
def create_user(**kwargs):
    defaults = {
        "username": "afein",
        "password": "dummy",
        "email": "nalfemp@gmail.com"
    }
    defaults.update(kwargs)
    return User.objects.create(**defaults)


class SpyglassViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_GET_index(self):
        resp = self.client.get(reverse('receive_query'))
        self.assertEqual(resp.status_code, 302)
        # TODO: check GET of future views

    def test_POST_old_user(self):
        request = self.factory.post(reverse('receive_query'))
        request.user = create_user(email="oldemail@mail.com")
        request.POST = { 'params':'query text',
                  'email': request.user.email,
                  'site': 1,
                  'persistent':True }

        response = receive_query(request)

        self.assertEqual(response.status_code, 302)
        query = Query.objects.get(params="query text")
        self.assertEqual(query.user, request.user);
        self.assertEqual(query.params, request.POST['params']);
        self.assertEqual(query.site.pk, 1);

