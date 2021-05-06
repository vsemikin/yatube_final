from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """The model describes the fields, search and
    filters of the publication object in the admin panel."""
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """The model describes the fields and
    community searches in the admin panel."""
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
