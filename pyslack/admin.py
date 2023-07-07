from django.contrib import admin
from .models import SlackTeam, SlackUser, SlackChannel, SlackHistory, SlackMentions

# Register your models here.
@admin.register(SlackTeam)
class SlackTeamAdmin(admin.ModelAdmin):
    list_display=('team_id', 'name', 'url', 'domain', 'email_domain')

@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display=('user_id', 'team', 'name', 'is_admin', 'is_bot', 'display_name')

@admin.register(SlackChannel)
class SlackChannelAdmin(admin.ModelAdmin):
    list_display=('channel_id', 'name', 'unlinked', 'created')

@admin.register(SlackHistory)
class SlackHistoryAdmin(admin.ModelAdmin):
    list_display=('type', 'subtype', 'text', 'channel', 'user', 'inviter', 'ts')
    sortable_by=('ts', 'type')

@admin.register(SlackMentions)
class SlackMentionAdmin(admin.ModelAdmin):
    list_display=('message', 'mention_to')