from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに使用されています。")
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)