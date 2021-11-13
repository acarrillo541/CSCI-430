# Generated by Django 2.2.12 on 2021-11-12 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20211111_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
