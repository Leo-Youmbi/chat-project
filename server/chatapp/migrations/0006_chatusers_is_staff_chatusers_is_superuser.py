# Generated by Django 5.0.1 on 2024-01-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_alter_chatusers_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatusers',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatusers',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
