# Generated by Django 4.0.3 on 2022-03-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(unique=True),
        ),
    ]
