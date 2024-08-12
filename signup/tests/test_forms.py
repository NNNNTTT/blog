from django.test import TestCase, Client
from ..models import User
from ..forms import UserCreateForm

class UserCreateFormTest(TestCase):
    #フォームに有効なデータを提供し、フォームが有効であることを確認します。
    #フォームを保存してユーザーが正しく作成されることを確認します。
    def test_form_valid(self):
        form_data = {
            "email":"test@gmail.com",
            "password1":"tsubota_naoki",
            "password2":"tsubota_naoki"
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email,"test@gmail.com")
        self.assertTrue(user.check_password("tsubota_naoki"))

    #無効なメールアドレス（空のメール）を提供し、フォームが無効であることを確認します。
    #emailフィールドにエラーが含まれていることを確認します。
    def test_form_invalid_email(self):
        form_data = {
            'email': '',
            'password1': 'tsubota_naoki',
            'password2': 'tsubota_naoki'
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    #異なるパスワードを提供し、フォームが無効であることを確認します。
    #password2フィールドにエラーが含まれていることを確認します。
    def test_form_password_mismatch(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'tsubota_naoki',
            'password2': 'naoki'
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    #すでに存在するメールアドレスを使用してフォームを送信し、フォームが無効であることを確認します。
    #emailフィールドにエラーが含まれていることを確認します。
    def test_form_duplicate_email(self):
        User.objects.create_user(email="test@gmail.com",password="tsubota_naoki")
        form_data = {
            "email":"test@gmail.com",
            "password1":"tsubota_naoki",
            "password2":"tsubota_naoki"
        }
        form = UserCreateForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email",form.errors)
    




