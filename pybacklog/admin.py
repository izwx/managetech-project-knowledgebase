from django.contrib import admin
from .models import BacklogUser, BacklogProject, BacklogVersion, BacklogIssue, BacklogWiki

# Register your models here.
@admin.register(BacklogUser)
class BacklogUserAdmin(admin.ModelAdmin):
    list_display = ('m_developer_id', 'backlogId', 'name', 'mailAddress')

@admin.register(BacklogProject)
class BacklogProjectAdmin(admin.ModelAdmin):
    list_display = ('m_project_id', 'projectId', 'name',)

@admin.register(BacklogVersion)
class BacklogVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'versionId', 'name',)

@admin.register(BacklogIssue)
class BacklogIssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'issueId', 'summary',)

@admin.register(BacklogWiki)
class BacklogWikiAdmin(admin.ModelAdmin):
    list_display = ('project', 'wikiId', 'name',)