# Generated by Django 3.1.4 on 2020-12-17 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='place',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]