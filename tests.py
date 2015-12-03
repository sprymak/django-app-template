from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status


class {{ app_name|title }}TestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_anonymous_can_get_article_list(self):
        response = self.client.get(reverse('{{ app_name }}-article-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
