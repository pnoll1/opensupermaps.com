from __future__ import unicode_literals

from django.contrib import admin
from .models import subscription, subscriptionFix, transaction
from markdownx.admin import MarkdownxModelAdmin

myModels = [subscription, subscriptionFix, transaction]
admin.site.register(myModels)
