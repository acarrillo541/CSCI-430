from feed.models import FeedItem, Like, DisLike
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
class FeedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = FeedItem
        fields = '__all__'
class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = Like
        fields = '__all__'
class DisLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = DisLike
        fields = '__all__'
