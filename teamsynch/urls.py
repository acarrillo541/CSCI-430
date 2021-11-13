"""FootballPool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from feed import views as feed_views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('join/', core_views.join, name='join'),
    path('login/', core_views.user_login, name='user_login'),
    path('logout/', core_views.user_logout, name='user_logout'),
    path('creategroup/', core_views.creategroup, name='creategroup'),
    path('joingroup/', core_views.joingroup, name='joingroup'),
    path('about/', core_views.about, name='about'),
    path('feed/', feed_views.home, name='feed'),
    path('like/', feed_views.like_post, name='likecomment'),
    path('dislike/', feed_views.dis_like_post, name='dislikecomment'),
    path('settings/', core_views.settings, name='settings'),
    path("group/<int:id>", core_views.group, name='group'),
    path("groupdel/<int:id>", core_views.leavegroup, name='groupdel'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
