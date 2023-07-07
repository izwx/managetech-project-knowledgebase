from django.contrib import admin
from .models import ChatworkConfiguration, ChatworkMember, ChatworkRoom, ChatworkMention, ChatworkTask, ChatworkMessage, ChatworkFile

# Register your models here.
@admin.register(ChatworkConfiguration)
class ChatworkConfigurationAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_token')

@admin.register(ChatworkRoom)
class ChatworkRoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'name', 'type')

@admin.register(ChatworkMember)
class ChatworkMemberAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'name', 'role', 'chatwork_id')

@admin.register(ChatworkMessage)
class ChatworkMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'account', 'body', 'room', 'send_time', 'update_time')
    sortable_by = ('send_time', 'update_time')

@admin.register(ChatworkMention)
class ChatworkMentionAdmin(admin.ModelAdmin):
    list_display = ('message', 'mention_to',)

@admin.register(ChatworkFile)
class ChatworkFileAdmin(admin.ModelAdmin):
    list_display = ('file_id', 'message_id', 'account', 'filename', 'room')

@admin.register(ChatworkTask)
class ChatworkTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'message_id', 'account', 'assigned_by_account', 'body', 'status', 'room')