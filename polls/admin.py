from django.contrib import admin

from .models import Poll

class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'pub_date')

admin.site.register(Poll, PollAdmin)
