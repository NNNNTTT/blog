from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", )

    def __int__(self, *args, **kwargs) -> None:
        super().__int__(*args, **kwargs)