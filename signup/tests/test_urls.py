from django.test import TestCase
from django.urls import reverse, resolve
from signup.views import *

class TestsUrls(TestCase):
    """ indexの関数が呼び出せているかテスト """
    def test_index_url(self):
        url = reverse('signup:index')
        # url.funcが、indexと等しいかどうか
        self.assertEqual(resolve(url).func, index)

    def test_login_url(self):
        url = reverse('signup:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url(self):
        url = reverse('signup:logout')
        self.assertEqual(resolve(url).func, logout_view)

