from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# from django.utils.crypto import get_random_string >>> this needs to go into groups


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(
        default="yoda.png", null=True, blank=True)
    form_submit = models.BooleanField(default = False)


class Group(models.Model):  # unique league
   group_name = models.CharField(max_length=30)
   group_id = models.CharField(max_length=10)
   group_creator = models.ForeignKey(
       User, on_delete=models.CASCADE, related_name="creator")  # only 1 user
   group_members = models.ManyToManyField(User)

class Task(models.Model): # belongs to a group 
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(
       User, on_delete=models.CASCADE, related_name="owner", null=True) 
    task_name = models.CharField(max_length=30)

