# Generated by Django 2.2.9 on 2020-05-17 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_auto_20200513_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targettype',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
