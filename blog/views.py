from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Article
from .forms import ArticleCreateForm

# Create your views here.
def article_view(request):
    articles = Article.objects.all().order_by("-created_at")
    context = {"articles":articles}
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
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            articles = Article.objects.all().order_by("-created_at")
            context = {"articles":articles}
            return render(request, "blog/article.html",context)
        
        return render(request,"blog/create.html",)
    
@login_required
def admin(request):
    if request.method == "GET":
        articles = Article.objects.filter(author=request.user).order_by("-created_at")
        context = {"articles":articles,"admin":True}
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
        context = {"articles":articles,"admin":True}
    return render(request,"blog/article.html", context)
