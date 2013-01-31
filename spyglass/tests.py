from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class SpyglassViewsTestCase(TestCase):
        def test_GET_index(self):
            resp = self.client.get(reverse('receive_query'))
            self.assertEqual(resp.status_code, 302)
            # TODO: check GET of future views
