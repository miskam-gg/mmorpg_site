# Generated by Django 5.0.4 on 2024-04-07 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='author',
        ),
        migrations.RemoveField(
            model_name='response',
            name='sender_id',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
