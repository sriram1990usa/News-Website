# Generated by Django 3.2.5 on 2022-06-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_article_weekly_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='today_headlines',
            field=models.BooleanField(default=False),
        ),
    ]
