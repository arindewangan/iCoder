# Generated by Django 4.0.4 on 2022-04-23 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='blog/thumbnails'),
        ),
    ]
