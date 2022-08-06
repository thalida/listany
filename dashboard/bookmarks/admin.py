# Listany - Copyright (C) 2022  Thalida Noel
from django.contrib import admin
from bookmarks.models import Bookmark, Link, Collection

admin.site.register(Bookmark)
admin.site.register(Link)
admin.site.register(Collection)
