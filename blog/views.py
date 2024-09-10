from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Article
from .forms import ArticleCreateForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import pyheif

def convert_heic_to_jpeg(uploaded_file):
    if uploaded_file.name.lower().endswith('.heic'): #ファイル名が '.heic' で終わるかチェックします。つまり、HEIC形式のファイルか判定しています。
        # HEIC形式の画像を読み込む
        heif_file = pyheif.read(uploaded_file)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        # JPEG形式に変換
        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            'FileField',
            uploaded_file.name.replace('.heic', '.jpeg'),
            'image/jpeg',
            output.getbuffer().nbytes,
            None
        )
    else:
        return uploaded_file

# Create your views here.
def article_view(request):
    if request.method == "GET":
        articles = Article.objects.all().order_by("-created_at")
        paginator = Paginator(articles, 10) # 1ページに10件表示
        p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        articles = paginator.get_page(p) # 指定のページのArticleを取得
        num_list = list(paginator.page_range)
    context = {"articles":articles,"num_list":num_list}
    return render(request,"blog/article.html",context)

def search(request):
    if request.method == "GET":
        search_text = request.GET.get('search', '')
        print(search_text)
        search_articles = Article.objects.filter(title__contains = search_text).order_by("-created_at")
        paginator = Paginator(search_articles, 10) # 1ページに10件表示
        p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        search_articles = paginator.get_page(p) # 指定のページのArticleを取得
        num_list = list(paginator.page_range)

    else:
        search_text = request.POST["search"]
        search_articles = Article.objects.filter(title__contains = search_text).order_by("-created_at")
        paginator = Paginator(search_articles, 10) # 1ページに10件表示
        p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        search_articles = paginator.get_page(p) # 指定のページのArticleを取得
        num_list = list(paginator.page_range)
    context = {"articles":search_articles,"search_text":search_text,"num_list":num_list}
    return render(request,"blog/article.html",context)


def detail(request, pk: int):
    article = Article.objects.get(pk=pk)
    context = {"article":article}
    return render(request,"blog/detail.html",context)

@login_required
def create(request):
    if request.method == "GET":
        context = {"form":ArticleCreateForm}
        return render(request,"blog/create.html",context)
    else:
        form = ArticleCreateForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            changed_fields = form.changed_data
            if "picture" in changed_fields:
                file = form.cleaned_data['picture']
                file = convert_heic_to_jpeg(file)
                article.picture = file
            article.save()
            return HttpResponseRedirect(reverse("blog:article"))
        
        return render(request,"blog/create.html",)
    
@login_required
def admin(request):
    if request.method == "GET":
        articles = Article.objects.filter(author=request.user).order_by("-created_at")
        paginator = Paginator(articles, 10) # 1ページに10件表示
        p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        articles = paginator.get_page(p) # 指定のページのArticleを取得
        num_list = list(paginator.page_range)
        context = {"articles":articles,"admin":True,"num_list":num_list}
        return render(request,"blog/article.html",context)
    
@login_required
def edit(request, pk: int):
    if request.method == "GET":
        article = Article.objects.get(author=request.user, pk=pk)
        context = {"article":article}
        return render(request,"blog/edit.html",context)

@login_required
def update_or_delete(request, pk: int):
    if request.method == "POST":
        article = Article.objects.get(author=request.user, pk=pk)
        if "update" in request.POST:         
            article.title = request.POST["title"]
            article.body = request.POST["body"]
            article.save()
        elif "delete" in request.POST:
            article.delete()
        articles = Article.objects.filter(author=request.user).order_by("-created_at")
        paginator = Paginator(articles, 10) # 1ページに10件表示
        p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        articles = paginator.get_page(p) # 指定のページのArticleを取得
        num_list = list(paginator.page_range)
        context = {"articles":articles,"admin":True,"num_list":num_list}
    return render(request,"blog/article.html", context)
