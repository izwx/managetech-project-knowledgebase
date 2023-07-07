from django.contrib import admin
from .models import ConfluenceUser, ConfluenceSpace, ConfluencePage

# Register your models here.
@admin.register(ConfluenceUser)
class ConfluenceUserAdmin(admin.ModelAdmin):
    list_display = ('m_developer_id', 'domain_url', 'accountId', 'publicName', 'displayName')


@admin.register(ConfluenceSpace)
class ConfluenceSpaceAdmin(admin.ModelAdmin):
    list_display = ('m_project_id', 'domain_url', 'spaceId', 'spaceKey', 'name')

@admin.register(ConfluencePage)
class ConfluencePageAdmin(admin.ModelAdmin):
    list_display = ('domain_url', 'pageId', 'title')
