# Generated by Django 4.2.1 on 2023-06-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_app', '0002_remove_podcast_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='author',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]