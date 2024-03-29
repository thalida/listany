# Generated by Django 4.1.7 on 2023-04-06 01:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0005_alter_usertag_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="link",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="links",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
