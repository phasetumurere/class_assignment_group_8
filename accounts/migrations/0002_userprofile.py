# Generated by Django 3.1 on 2023-02-07 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(blank=True, max_length=200)),
                ('address_line_2', models.CharField(blank=True, max_length=200)),
                ('profile_picture', models.ImageField(blank=True, upload_to='photos/userprofile/')),
                ('city', models.CharField(blank=True, max_length=200)),
                ('district', models.CharField(blank=True, max_length=200)),
                ('country', models.CharField(blank=True, max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
