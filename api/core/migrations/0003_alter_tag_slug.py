# Generated by Django 4.1.7 on 2023-04-02 20:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_tag_unique_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(editable=False, max_length=2000),
        ),
    ]
