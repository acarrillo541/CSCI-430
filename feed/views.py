from django.shortcuts import render, redirect
from feed.forms import FeedForm
from feed.models import FeedItem, Like, DisLike
from core.models import Group
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from feed.serializers import FeedItemSerializer, LikeSerializer, DisLikeSerializer, UserSerializer
def home(request):
    context = {"form":FeedForm, "comment_list":[], "groups":[]}
    comment_list = FeedItem.objects.all()
    context["comment_list"] = comment_list
    if request.method == 'POST' and 'addcomment' in request.POST:
        form = FeedForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            FeedItem(user = request.user,name = request.user,comment = comment, profile_picture = request.user.userprofile.profile_picture).save()
            Groups = Group.objects.all()
            for group in Groups:
                if request.user in group.group_members.all():
                    context['groups'].append(group)
                    print("True")
            return redirect('/feed/')
        else:
            groups = Group.objects.all()
            for group in groups:
                if request.user in group.group_members.all():
                    context['groupss'].append(group)
                    print("True")
            context["form"] = form
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return render(request, "feed/home.html", context)

def like_post(request):
    context = {'groups': []}
    user = request.user
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        feed_item = FeedItem.objects.get(id=comment_id)
        if user in feed_item.liked.all():
            feed_item.liked.remove(user)
        else:
            feed_item.disliked.remove(user)
            feed_item.liked.add(user)
        like, created = Like.objects.get_or_create(user=request.user, comment_id = comment_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return redirect('/feed/')


def dis_like_post(request):
    context = {'groups': []}
    user = request.user
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        feed_item = FeedItem.objects.get(id=comment_id)
        if user in feed_item.disliked.all():
            feed_item.disliked.remove(user)
        else:
            feed_item.liked.remove(user)
            feed_item.disliked.add(user)
        dislike, created = DisLike.objects.get_or_create(user=request.user, comment_id = comment_id)
        if not created:
            if dislike.value == 'Dislike':
                dislike.value = 'Un-dislike'
            else:
                dislike.value = 'Dislike'
        dislike.save()
    groups = Group.objects.all()
    for group in groups:
        if request.user in group.group_members.all():
            context['groups'].append(group)
            print("True")
    return redirect('/feed/')
class FeedItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer
    permission_classes = [permissions.IsAuthenticated]
class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
class DisLikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = DisLike.objects.all()
    serializer_class = DisLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
