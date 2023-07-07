from django.contrib import admin
from .models import RedmineProject, RedmineUser, RedmineTracker, RedminePriority, RedmineStatus, RedmineIssue, RedmineFile
from .models import RedmineWiki, RedmineVersion

# Register your models here.

@admin.register(RedmineProject)
class RedmineProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name', 'domain_url', )

@admin.register(RedmineUser)
class RedmineUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'login', 'domain_url', )

@admin.register(RedmineTracker)
class RedmineTrackerAdmin(admin.ModelAdmin):
    list_display = ('tracker_id', 'name', 'domain_url', )

@admin.register(RedminePriority)
class RedminePriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_id', 'name', 'domain_url', )

@admin.register(RedmineStatus)
class RedmineStatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'name', 'domain_url', 'is_closed')

@admin.register(RedmineIssue)
class RedmineIssueAdmin(admin.ModelAdmin):
    list_display = ('issue_id', 'subject', 'domain_url', 'author')

@admin.register(RedmineFile)
class RedmineFileAdmin(admin.ModelAdmin):
    list_display = ('file_id', 'filename', 'domain_url', 'author')

@admin.register(RedmineWiki)
class RedmineWikiAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'domain_url', 'author')

@admin.register(RedmineVersion)
class RedmineVersionAdmin(admin.ModelAdmin):
    list_display = ('version_id', 'project', 'domain_url', 'name')