# Generated by Django 3.2.5 on 2022-06-11 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='breaking_news',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='trending',
            field=models.BooleanField(default=False),
        ),
    ]
