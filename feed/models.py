from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FeedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author')
    name = models.CharField(max_length = 255)
    comment = models.CharField(max_length = 255)
    date = models.DateTimeField(auto_now_add = True)
    liked = models.ManyToManyField(User, default = None, blank = True, related_name = 'liked')
    disliked = models.ManyToManyField(User, default = None, blank = True, related_name = 'disliked')
    profile_picture = models.ImageField(default="yoda.png", null=True, blank=True)


    @property
    def num_likes(self):
        return self.liked.all().count()

CHOICES=(
('Like', 'Like'),
('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(FeedItem, on_delete=models.CASCADE)
    value = models.CharField(choices = CHOICES, default='Like', max_length = 10)

    def __str__(self):
        return str(self.comment)


class DisLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(FeedItem, on_delete=models.CASCADE)
    value = models.CharField(choices = CHOICES, default='DisLike', max_length = 10)

    def __str__(self):
        return str(self.comment)
