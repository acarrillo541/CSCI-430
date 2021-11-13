from django.shortcuts import render, redirect
from core.forms import JoinForm, LoginForm, CreateGroupForm, JoinGroup, EditSettings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.models import UserProfile, Group
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from feed.models import FeedItem
import requests
import json
from django.contrib import messages
from datetime import datetime, timedelta
from pytz import timezone
import requests
import json
import pytz


@login_required(login_url='/login/')
def home(request):
    context = {'groups': []}
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return render(request, "core/home.html",context)


def about(request):
    context = {"groups": []}
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return render(request, "core/about.html", context)


def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            user = join_form.save()
            UserProfile.objects.create(
                user=user, first_name=user.first_name, last_name=user.last_name, email=user.email)
            user.set_password(user.password)
            user.save()
            return redirect("/")
        else:
            page_data = {"join_form": join_form}
            return render(request, 'core/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'core/join.html', page_data)


def user_login(request):
    context = {"messages": "", "login_form": LoginForm}
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    try:
                        UserProfile.objects.get(user=user)
                    except:
                        UserProfile.objects.create(
                            user=user, first_name=user.first_name, last_name=user.last_name, email=user.email)

                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                context["messages"] = "Invalid username or password"
                return render(request, 'core/login.html', context)
    else:
        return render(request, 'core/login.html', context)


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")


def creategroup(request):
    context = {"form": CreateGroupForm,
               "group_name": str, "group_id": str, "groups": []}
    if request.method == 'POST' and 'creategroup' in request.POST:
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            context["group_name"] = form.cleaned_data["group_name"]
            context["group_id"] = get_random_string(10)
            new_group = Group(
                group_name=context["group_name"], group_creator=request.user, group_id=context["group_id"])
            new_group.save()
            users = UserProfile.objects.filter(user=request.user).all()
            for user in users:
                new_group.group_members.add(user.user)
            new_group.save()
            new_group.save
            path = '/group/' + str(new_group.id)
            groups = Group.objects.all()
            for group in groups:
                if request.user in group.group_members.all():
                    context['groups'].append(group)
            return redirect(path)
        else:
            context["form"] = form
    elif request.method == 'GET' and 'cancel' in request.GET:
        groups = Group.objects.all()
        for group in groups:
            if request.user in group.group_members.all():
                context['groups'].append(group)
        return redirect('/')
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(groups)
    return render(request, "core/creategroup.html", context)


def joingroup(request):
    context = {"form": JoinGroup, "groups": []}
    if request.method == 'POST' and 'joingroup' in request.POST:
        form = JoinGroup(request.POST)
        if form.is_valid():
            group_id = form.cleaned_data["group_id"]
            try:
                group_join = Group.objects.get(group_id=group_id)
                print(group_join)
            except:
                print("Group Doesnt Exist")
            group_join.save()
            if request.user in group_join.group_members.all():
                return render(request, "core/joingroup.html", context)
            else:
                group_join.group_members.add(request.user)
                groups = Group.objects.all()
                for group in groups:
                    if request.user in group.group_members.all():
                        context['groups'].append(group)
                        print("True")
                print("Member added to Group")
            group_join.save()
            path = '/group/' + str(group_join.id)
            groups = Groups.objects.all()
            for group in groups:
                if request.user in group.group_members.all():
                    context['groups'].append(group)
            return redirect(path)
        else:
            context["form"] = form
    elif request.method == 'GET' and 'cancel' in request.GET:
        return redirect('/')
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
    return render(request, "core/joingroup.html", context)


def leavegroup(request, id):
    group = Group.objects.get(id=id)
    group.group_members.remove(request.user)
    return redirect('/')


def settings(request):
    try:
        user = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user = UserProfile.objects.create(
            user=request.user, first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)

    form = EditSettings(instance=user)
    if request.method == 'POST' and 'update' in request.POST:
        form = EditSettings(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            comments = FeedItem.objects.filter(user=request.user)
            for comment in comments:
                comment.profile_picture = user.profile_picture
                comment.save()
    context = {'form': form, "groups": []}
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return render(request, 'core/settings.html', context)


def group(request, id):
    context = {"group_details": [], "groups": []}
    group1 = Group.objects.get(id=id)
    context["group_details"] = group1
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return render(request, "core/group.html", context)
