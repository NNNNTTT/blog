from django.test import TestCase
from django.urls import reverse,resolve
from blog.views import *

class TestUrls(TestCase):
    #指定のurlsからviewsの関数の呼び出しが正常に行われているか確認する
    def test_article_url(self):
        url = reverse('blog:article')
        # url.funcが、indexと等しいかどうか
        self.assertEqual(resolve(url).func, article_view)

    def test_detail_url(self):
        url = reverse('blog:detail',args=[1])
        self.assertEqual(url,"/blog/1/")
        self.assertEqual(resolve(url).func, detail)

    def test_create_url(self):
        url = reverse('blog:create')
        self.assertEqual(resolve(url).func, create)

    def test_admin_url(self):
        url = reverse('blog:admin')
        self.assertEqual(resolve(url).func, admin)

    def test_edit_url(self):
        url = reverse("blog:edit",args=[1])
        self.assertEqual(url,"/blog/admin/1/")
        self.assertEqual(resolve(url).func, edit)
        print()

    def test_update_or_delete_url(self):
        url = reverse("blog:update_or_delete",args=[1])
        self.assertEqual(url,"/blog/admin/update_or_delete/1/")
        self.assertEqual(resolve(url).func, update_or_delete)