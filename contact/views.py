from django.shortcuts import render
from django.views import View
from .forms import ContactForm
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

class ContactView(View):
    def get(self, request, *args, **kwargs):
        context = {"form":ContactForm(),}
        return render(request, "contact/contact.html", context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if not form.is_valid():
            context = {"form":form,"message":"※お名前を20文字以下、または正しいEメールアドレスを入力してください"}
            return render(request, "contact/contact.html", context)
        form.save()
        return render(request, "contact/contact_ok.html")
    
contact_view = ContactView.as_view()

class Contact_Ok_View(View):
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("blog:article"))
    
contact_ok_view = Contact_Ok_View.as_view()