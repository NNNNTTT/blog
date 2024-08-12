from django.test import TestCase
from ..models import Article

# Create your tests here.

class ArticleTests(TestCase):

    def test_validate_title(self):
        n = 30
        title = "".join([
            "a" for _ in range(n)
        ])
        article = Article(title=title)
        self.assertIs(article.validate_title(),True, "テストエラー")

    def test_validate_title_err(self):
        n = 31
        title = "".join([
            "a" for _ in range(n)
        ])
        article = Article(title=title)
        self.assertIs(article.validate_title(),False, "テストエラー")
        