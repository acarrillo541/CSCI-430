from django.contrib import admin
from core.models import UserProfile
from core.models import Group
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Group)
