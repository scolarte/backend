# Generated by Django 3.0.2 on 2020-02-16 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0010_list_seller_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='list_image',
            field=models.FileField(blank=True, null=True, upload_to='lists_images'),
        ),
    ]
