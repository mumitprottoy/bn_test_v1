# Generated by Django 5.2.2 on 2025-06-07 12:26

import player.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_remove_xpmap_trigger_xpmap_trigger_codename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[player.models.forbidden_word_validator]),
        ),
    ]
