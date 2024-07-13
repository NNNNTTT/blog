from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreateForm
# Create your views here.

def index(request):
    if request.method == "GET":
        context = {"form":UserCreateForm}
        return render(request, "signup/home.html",context)
    form = UserCreateForm(request.POST)

    if form.is_valid():
        form.save()
        return render(request, "signup/home.html")
    else:
        return render(request, "signup/home.html", {"form":form})

def login_view(request):
    if request.method == "GET":
        return render(request,"signup/login.html")
    
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)
    login(request, user)
    return render(request,"signup/login.html")

def logout_view(request):
    logout(request)
    return render(request,"signup/login.html")
