from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreateForm,UserNameForm
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    if request.method == "GET":
        context = {"form":UserCreateForm()}
        return render(request, "signup/home.html",context)
    form = UserCreateForm(request.POST)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return render(request, "signup/username_create.html")
    else:
        error_messages = form.errors.get('email', [])
        if 'このメールアドレスはすでに使用されています。' in error_messages:
        # メールアドレスの重複エラーに特化したメッセージを表示する
            error_message = "このメールアドレスはすでに使用されています。別のメールアドレスを使用してください。"
        else:
            error_message = "メールアドレス、パスワードを正しく入力してください"

        return render(request, "signup/home.html", {"form":form,"message":error_message})

@login_required       
def signup_ok(request):
    request.method == "POST"
    return HttpResponseRedirect(reverse("blog:article"))

def login_view(request):
    if request.method == "GET":
        return render(request,"signup/login.html")
    
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("blog:article"))
    else:
        error_message = "ログインに失敗しました。メールアドレスまたはパスワードが正しくありません。"
        return render(request, "signup/login.html",{"error_message":error_message})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("blog:article"))

def username_create(request):
    if request.method == "GET":
        context = {"form":UserNameForm()}
        return render(request, "signup/username_create.html",context)
    
    form = UserNameForm(request.POST)
    
        # フォームのエラーとデータをログに出力
    if not form.is_valid():
        print(form.errors)

    if form.is_valid():
        user = request.user
        username = form.cleaned_data["username"]
        user.username = username
        user.save()
        return render(request, "signup/signup_ok.html")
    
    context = {"message":"ユーザーネームが正しくありません"}
    return render(request,"signup/username_create.html",context)
    
