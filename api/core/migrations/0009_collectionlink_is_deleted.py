# Generated by Django 4.1.7 on 2023-04-06 01:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_collection_is_deleted_collection_is_hidden"),
    ]

    operations = [
        migrations.AddField(
            model_name="collectionlink",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
