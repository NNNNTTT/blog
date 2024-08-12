from django.test import TestCase
from ..forms import ArticleCreateForm
from ..models import Article

class ArticleCreateFormTests(TestCase):

    def test_valid_form(self):
        # 有効なデータを用いてフォームを作成
        data = {
            "title": "Test Article",
            "body": "This is a test article."
        }
        form = ArticleCreateForm(data=data)
        
        # フォームが有効であることを確認
        self.assertTrue(form.is_valid())

        # フォームを保存し、データベースに保存された記事が正しいことを確認
        article = form.save()
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.body, "This is a test article.")

    def test_invalid_form_empty_title(self):
        # タイトルが空の場合のテスト
        data = {
            "title": "",
            "body": "This is a test article."
        }
        form = ArticleCreateForm(data=data)
        
        # フォームが無効であることを確認
        self.assertFalse(form.is_valid())

        # フォームが適切なエラーメッセージを返すことを確認
        self.assertIn("title", form.errors)
        self.assertEqual(form.errors["title"], ["This field is required."])

    def test_invalid_form_empty_body(self):
        # ボディが空の場合のテスト
        data = {
            "title": "Test Article",
            "body": ""
        }
        form = ArticleCreateForm(data=data)
        
        # フォームが無効であることを確認
        self.assertFalse(form.is_valid())

        # フォームが適切なエラーメッセージを返すことを確認
        self.assertIn("body", form.errors)
        self.assertEqual(form.errors["body"], ["This field is required."])
