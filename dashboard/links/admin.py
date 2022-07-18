from django.contrib import admin
from links.models import Link, LinkMeta, Collection

admin.site.register(Link)
admin.site.register(LinkMeta)
admin.site.register(Collection)
