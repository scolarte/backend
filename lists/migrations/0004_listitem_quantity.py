# Generated by Django 3.0.2 on 2020-01-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_list_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=4, null=True),
        ),
    ]
