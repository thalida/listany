# Generated by Django 3.2.14 on 2022-07-18 22:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_auto_20220718_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='description',
        ),
        migrations.RemoveField(
            model_name='link',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='link',
            name='image',
        ),
        migrations.RemoveField(
            model_name='link',
            name='image_alt',
        ),
        migrations.RemoveField(
            model_name='link',
            name='link_type',
        ),
        migrations.RemoveField(
            model_name='link',
            name='title',
        ),
        migrations.CreateModel(
            name='LinkMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('icon', models.ImageField(blank=True, default=None, null=True, upload_to='links/icons/')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='links/images/')),
                ('image_alt', models.TextField(blank=True, default=None, null=True)),
                ('link_type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('robot_fetch_meta_allowed', models.BooleanField(default=True)),
                ('robot_fetch_icon_allowed', models.BooleanField(default=True)),
                ('robot_fetch_image_allowed', models.BooleanField(default=True)),
                ('robot_fetched_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='link_meta', to='links.link')),
            ],
        ),
    ]
