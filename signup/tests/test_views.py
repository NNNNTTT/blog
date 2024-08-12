from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from django.contrib.auth import get_user_model
from signup.forms import UserCreateForm

class ViewsTests(TestCase):
    #テストユーザー情報を一時的に登録する　テストメソッドが実行される前に呼び出される
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="admin@gmail.com",password="admin")

    #ユーザー情報が登録されているかを確認する
    def test_user_creation(self):
        self.assertEqual(self.user.email,"admin@gmail.com")
        self.assertTrue(self.user.check_password('admin'))  # ハッシュ化されたパスワードとプレーンテキストのパスワードを比較

    #getリクエストでview関数indexが動いているかテストする
    def test_index_get(self):
        response = self.client.get(reverse("signup:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/home.html")
        self.assertIsInstance(response.context["form"],UserCreateForm)

    #postリクエストでview関数indexが動いているか、ユーザー情報が登録されているかを確認する
    def test_index_post_valid(self):
        response = self.client.post(reverse("signup:index"),{
            "email":"test@gmail.com",
            "password1":"tsubota_naoki",
            "password2":"tsubota_naoki"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/signup_ok.html")
        self.assertTrue(User.objects.filter(email="test@gmail.com").exists())

    #ユーザー情報が登録できなかった場合の動きをテストしている
    def test_index_post_invalid(self):
        response = self.client.post(reverse("signup:index"),{
            "email":"test",
            "password1":"test",
            "password2":"test"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/home.html")
        self.assertFalse(User.objects.filter(email="test").exists())
        self.assertIsInstance(response.context["form"],UserCreateForm)

    #getリクエストでview関数login_viewが動いているかテストしている
    def test_login_view_get(self):
        response = self.client.get(reverse("signup:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/login.html")

    #postリクエストでview関数login_viewが動いているか、ログインが正常に行われているかテストしている
    def test_login_view_post_valid(self):
        response = self.client.post(reverse("signup:login"),{
            "email":"admin@gmail.com",
            "password":"admin"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("blog:article"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    #ログインでエラーが出た際の動きをテストしている
    def test_login_view_post_invalid(self):
        response = self.client.post(reverse("signup:login"),{
            "email":"test@gmail.com",
            "password":"test"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup/login.html")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    #view関数logout_viewが正常に動いているかテストしている
    def test_logout_view(self):
        self.client.login(email="admin@gmail.com",password="admin")
        response = self.client.get(reverse("signup:logout"))
        self.assertRedirects(response, reverse("blog:article"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        