from django.test import TestCase
from ..models import Article
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ArticleModelTests(TestCase):

    def setUp(self):
        # テスト用のユーザーを作成
        self.user = User.objects.create_user(email="test@gmail.com", password="tsubota_naoki")

        # テスト用の記事を作成
        self.article = Article.objects.create(
            author=self.user,
            title="Test Article",
            body="This is a test article.",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    def test_article_creation(self):
        # 記事が正常に作成されたことを確認
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.body, "This is a test article.")
        self.assertEqual(article.author, self.user)
        self.assertIsInstance(article.created_at, timezone.datetime)
        self.assertIsInstance(article.updated_at, timezone.datetime)

    def test_article_str(self):
        # __str__メソッドが期待通りの文字列を返すか確認
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(str(article), "Test Article")

    def test_article_default_created_at(self):
        # created_atフィールドがデフォルトで現在の日時になっているか確認
        article = Article.objects.get(id=self.article.id)
        now = timezone.now()
        self.assertLessEqual(article.created_at, now)

    def test_article_default_updated_at(self):
        # updated_atフィールドがデフォルトで現在の日時になっているか確認
        article = Article.objects.get(id=self.article.id)
        now = timezone.now()
        self.assertLessEqual(article.updated_at, now)

    def test_article_foreign_key_relation(self):
        # Articleが正しいユーザーに関連付けられているか確認
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(article.author, self.user)

    def test_article_update(self):
        # 記事の更新が正しく行われるかを確認
        article = Article.objects.get(id=self.article.id)
        article.title = "Updated Article"
        article.body = "This is an updated test article."
        article.save()
        self.assertEqual(article.title, "Updated Article")
        self.assertEqual(article.body, "This is an updated test article.")

    def test_article_deletion(self):
        # 記事が正常に削除されるかを確認
        article_id = self.article.id
        self.article.delete()
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=article_id)
