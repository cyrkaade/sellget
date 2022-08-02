from django.forms import ModelForm
from .models import Buy, myUser, Room
from django.contrib.auth.forms import UserCreationForm

# User forms that gain information about them

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = myUser
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['avatar', 'name', 'username', 'email']

class BuyForm(ModelForm):
    class Meta:
        model = Buy
        fields = ['quantity',]