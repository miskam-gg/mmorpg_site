from django.contrib import admin
from .models import Advertisement


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator')
    search_fields = ('title', 'category')
    list_filter = ('category',)

admin.site.register(Advertisement, AdvertisementAdmin)
