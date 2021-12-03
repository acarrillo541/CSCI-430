from django import forms
from django.contrib.auth.models import User
from core.models import Group, UserProfile, Task

class JoinForm(forms.ModelForm):
    username = forms.CharField(help_text=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreateGroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields = ['group_name']


class JoinGroup(forms.ModelForm):
    class Meta():
        model = Group
        fields = ['group_id']


class EditSettings(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'profile_picture']


class TaskEntryForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['task_name',]