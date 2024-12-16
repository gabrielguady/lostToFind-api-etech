

from django.contrib import admin

from core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active',)
    search_fields = ('id',)
    list_filter = ('is_active',)
    list_per_page = 50
    list_max_show_all = 5000