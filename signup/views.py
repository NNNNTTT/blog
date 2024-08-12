from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreateForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.method == "GET":
        context = {"form":UserCreateForm()}
        return render(request, "signup/home.html",context)
    form = UserCreateForm(request.POST)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return render(request, "signup/signup_ok.html")
    else:
        return render(request, "signup/home.html", {"form":form})

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
