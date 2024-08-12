from django.test import TestCase, Client
from ..models import User
from django.contrib.auth import get_user_model

c = Client()

class UserModelTests(TestCase):
    email = "admin@gmail"
    password = "admin"

    def setUp(self):
        #一時的にユーザーを作成する
        User.objects._create_user(self.email, self.password)

    #UserManagerクラスのcreate_userメソッドが正常に動いているかテストする
    def test_create_user(self):
        user = User.objects.create_user(email="test@gmail.com",password="tsubota_naoki")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.check_password("tsubota_naoki"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    #UserManagerクラスのcreate_superメソッドが正常に動いているかテストする
    def test_create_superuser(self):
        user = User.objects.create_superuser(email="superuser@gmail.com",password="tsubota_naoki")
        self.assertEqual(user.email, "superuser@gmail.com")
        self.assertTrue(user.check_password("tsubota_naoki"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    #メールアドレスの正規化が正しく行われることを確認します。
    def test_email_normalization(self):
        self.assertEqual(self.email,self.email.lower())

    #無効なメールアドレス（空文字列）でユーザーを作成しようとすると、ValueErrorが発生することを確認します。
    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="",password="tsubota_naoki")

    #スーパーユーザーがis_staff=Trueでなければ、ValueErrorが発生することを確認します。
    def test_superuser_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@gmail.com",
                password="tsubota_naoki",
                is_staff=False
            )

    #スーパーユーザーがis_superuser=Trueでなければ、ValueErrorが発生することを確認します。
    def test_superuser_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@gmail.com",
                password="tsubota_naoki",
                is_superuser=False
            )

    #ログインが正常に行えるか確認する
    def test_user_login(self):
        resp = c.login(email=self.email, password=self.password)
        print("resp:",resp)
        self.assertIs(resp, True)

    #emailが255文字以内の場合正常に登録できるか確認する
    def test_validate_email(self):
        domain = "@gmail.com"
        n = 255 - len(domain)
        email = "".join([
            "a" for _ in range(n)
        ]) + domain
        "aaa...@gmail.com"
        user = User(email=email)
        """
        user.validate_email() => True
        """
        self.assertIs(user.validate_email(), True, "エラー")

    #emailが255文字以上の場合は登録ができていないことを確認する
    def test_validate_email_err(self):
        domain = "@gmail.com"
        n = 256 - len(domain)
        email = "".join([
            "a" for _ in range(n)
        ]) + domain
        "aaa...@gmail.com"
        user = User(email=email)
        """
        user.validate_email() => True
        """
        self.assertIs(user.validate_email(), False,  "エラー")

    