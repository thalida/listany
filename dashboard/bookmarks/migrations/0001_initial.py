# Generated by Django 3.2.14 on 2022-07-19 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('icon', models.ImageField(blank=True, default=None, null=True, upload_to='links/icons/')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='links/images/')),
                ('image_alt', models.TextField(blank=True, default=None, null=True)),
                ('link_type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('is_fetch_allowed', models.BooleanField(blank=True, default=None, null=True)),
                ('is_fetch_icon_allowed', models.BooleanField(blank=True, default=None, null=True)),
                ('is_fetch_image_allowed', models.BooleanField(blank=True, default=None, null=True)),
                ('last_fetched_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_collections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collections', models.ManyToManyField(blank=True, default=None, related_name='links', to='bookmarks.Collection')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to=settings.AUTH_USER_MODEL)),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bookmarks.link')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(fields=('slug', 'created_by'), name='unique_collection_per_user'),
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(fields=('link', 'created_by'), name='unique_link_per_user'),
        ),
    ]
