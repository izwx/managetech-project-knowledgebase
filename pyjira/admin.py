from django.contrib import admin
from .models import JiraUser, JiraIssueType, JiraStatus, JiraPriority, JiraIssueComment, JiraIssue, JiraProject, JiraBoard, JiraSprint

# Register your models here.

@admin.register(JiraUser)
class JiraUserAdmin(admin.ModelAdmin):
    list_display=('accountId', 'emailAddress', 'displayName', 'self_url')

@admin.register(JiraBoard)
class JiraBoardAdmin(admin.ModelAdmin):
    list_display=('board_id', 'self_url', 'name', 'type', 'project')

@admin.register(JiraSprint)
class JiraSprintAdmin(admin.ModelAdmin):
    list_display=('sprint_id', 'self_url', 'state', 'name', 'startDate', 'endDate', 'board', 'goal')

@admin.register(JiraIssueType)
class JiraIssueTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(JiraStatus)
class JiraStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(JiraPriority)
class JiraPriorityAdmin(admin.ModelAdmin):
    pass

@admin.register(JiraIssueComment)
class JiraIssueCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(JiraIssue)
class JiraIssueAdmin(admin.ModelAdmin):
    pass

@admin.register(JiraProject)
class JiraProjectAdmin(admin.ModelAdmin):
    list_display=('uuid', 'self_url', 'project_id', 'key', 'name',)