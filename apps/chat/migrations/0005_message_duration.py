# Generated by Django 5.0.6 on 2024-05-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_message_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
