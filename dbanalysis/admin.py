from django.contrib import admin
from .models import DDeveloperToolMap, DProjectToolInfo, DBatchLog, DTool
from .models import DChannel, DMessage, DMention, DSprint, DPullRequest, DTicket, DDocument

# Register your models here.

@admin.register(DDeveloperToolMap)
class DDeveloperToolMapAdmin(admin.ModelAdmin):
    list_display = ('developer_id', 'tool_id', 'account_name',)

@admin.register(DProjectToolInfo)
class DProjectToolInfoAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'd_tool', 'tool_id', 'token', 'target', 'payload')

@admin.register(DBatchLog)
class DBatchLogAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'module', 'batch_type', 'start_datetime', 'end_datetime')

@admin.register(DTool)
class DToolAdmin(admin.ModelAdmin):
    list_display = ('tool_id', 'tool_name')

@admin.register(DChannel)
class DChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_uid', 'tool', 'name')

@admin.register(DMessage)
class DMessageAdmin(admin.ModelAdmin):
    list_display = ('message_uid', 'project', 'channel', 'contents', 'created_at')

@admin.register(DMention)
class DMentionAdmin(admin.ModelAdmin):
    list_display = ('mention_uid', 'message', 'mention_to', 'created_at')

@admin.register(DSprint)
class DSprintAdmin(admin.ModelAdmin):
    list_display = ('sprint_uid', 'name', 'project', 'start_date', 'status')

@admin.register(DTicket)
class DTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_uid', 'project', 'sprint', 'title', 'status', 'start_date')

@admin.register(DPullRequest)
class DPullRequestAdmin(admin.ModelAdmin):
    list_display = ('pull_request_uid', 'project', 'title', 'create_datetime', 'merge_datetime', )

@admin.register(DDocument)
class DDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_uid', 'project', 'title', 'created_at', 'updated_at',)