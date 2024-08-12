from django.test import TestCase, Client
from django.urls import reverse
from ..models import Article
from blog.forms import ArticleCreateForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleViewsTests(TestCase):
    def setUp(self):
        #各テストメソッドが実行される前に、テスト用のユーザーと記事を作成します。これにより、テストが一貫して実行できるようにします。
        self.client = Client()
        self.user = User.objects.create_user(email="test@gmail.com",password="tsubota_naoki")

        self.article1 = Article.objects.create(
            author = self.user,
            title = "article1",
            body = "body1"
        )

        self.article2 = Article.objects.create(
            author = self.user,
            title = "article2",
            body = "body2"
        )

        self.user2 = User.objects.create_user(email="test2gmail.com", password="tsubota_naoki")

        self.article3 = Article.objects.create(
            author = self.user2,
            title = "article3",
            body = "body3"
        )
    
    #GETリクエストに対してblog:articleビューの動作をテストします。
    def test_article_view_get(self):
        response = self.client.get(reverse("blog:article"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article.html")
        self.assertIn(self.article1, response.context["articles"])
        self.assertIn(self.article2, response.context["articles"])

    #POSTリクエストに対してblog:articleビューの動作をテストします。
    def test_article_view_post(self):
        response = self.client.post(reverse("blog:article"),{"search":"article1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article.html")
        self.assertIn(self.article1, response.context["articles"])
        self.assertNotIn(self.article2, response.context["articles"])

    #GETリクエストに対してblog:detailビューの動作をテストします。
    def test_detail(self):
        response = self.client.get(reverse('blog:detail', args = [self.article1.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(response.context['article'], self.article1)
        self.assertNotEqual(response.context["article"],self.article2)
    
    #ログイン済みユーザーによるGETリクエストでblog:createビューの動作をテストします。
    def test_create_get(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.get(reverse("blog:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/create.html")


    #ログインしていないユーザーによるGETリクエストでblog:createビューの動作をテストします。
    def test_create_get_not_login(self):
        response = self.client.get(reverse("blog:create"))
        self.assertEqual(response.status_code, 302)

    #ログイン済みユーザーによるPOSTリクエストでblog:createビューの動作をテストします。
    def test_create_post(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.post(reverse("blog:create"),{"title":"article4","body":"body4"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article.html")
        self.assertTrue(Article.objects.filter(title="article4").exists())  

    #ログイン済みユーザーによる無効なデータのPOSTリクエストでblog:createビューの動作をテストします。
    def test_create_post_invalid(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.post(reverse("blog:create"),{"title":"article4"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/create.html")
        self.assertFalse(Article.objects.filter(title="article4").exists()) 

    #ログイン済みユーザーによるGETリクエストでblog:adminビューの動作をテストします。
    def test_admin_get(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.get(reverse("blog:admin"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/article.html")
        articles = response.context["articles"]
        self.assertEqual(len(articles), 2)
        self.assertIn(self.article1, articles)
        self.assertIn(self.article2, articles)
        self.assertNotIn(self.article3, articles)

    #ログインしていないユーザーによるGETリクエストでblog:adminビューの動作をテストします。
    def test_admin_get_not_login(self):
        response = self.client.get(reverse("blog:admin"))
        self.assertEqual(response.status_code, 302)

    #ログイン済みユーザーによるGETリクエストでblog:editビューの動作をテストします。
    def test_edit_get(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.get(reverse("blog:edit",args = [self.article1.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/edit.html")
        self.assertContains(response, self.article1.title)
        self.assertContains(response, self.article1.body)

    #ログインしていないユーザーによるGETリクエストでblog:editビューの動作をテストします。
    def test_edit_get_not_login(self):
        response = self.client.get(reverse("blog:edit",args = [self.article1.author.pk]))
        self.assertEqual(response.status_code, 302)

    #ログイン済みユーザーによるPOSTリクエストでblog:update_or_deleteビューの更新機能をテストします。
    def test_update(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.post(reverse("blog:update_or_delete",args=[self.article1.pk]),
                                    {"title":"test", "body":"test","update":"update"})
        self.assertEqual(response.status_code, 200)
        self.article1.refresh_from_db()
        self.assertEqual(self.article1.title, "test")
        self.assertEqual(self.article1.body, "test")

    #ログイン済みユーザーによるPOSTリクエストでblog:update_or_deleteビューの削除機能をテストします。
    def test_delete(self):
        self.client.login(email="test@gmail.com", password="tsubota_naoki")
        response = self.client.post(reverse("blog:update_or_delete", args=[self.article1.pk]),
                                    {"delete":"delete"})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(pk=self.article1.pk)

    #ログインしていないユーザーによるPOSTリクエストでblog:update_or_deleteビューの動作をテストします。
    def test_update_or_delete_not_login(self):
        response = self.client.post(reverse("blog:update_or_delete",args=[self.article1.pk]))
        self.assertEqual(response.status_code, 302)

        