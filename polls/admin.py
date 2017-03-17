from django.contrib import admin

from .models import Poll

class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'pub_date')
    # exclude
    # readonly_fields 
admin.site.register(Poll, PollAdmin)
