from rest_framework import serializers
from django.db.models import Q
from .models import SlackHistory
from dbanalysis.models import DTool

from datetime import datetime
import pytz

class SlackChannelSerializer(serializers.Serializer):
    channel_uid = serializers.SerializerMethodField()
    def get_channel_uid(self, obj):
        return f"slack-channel-{obj.id}"

    project_id = serializers.IntegerField()
    
    tool_id = serializers.SerializerMethodField()
    def get_tool_id(self, obj):
        tool_info = DTool.objects.get(tool_name__iexact='slack')
        return tool_info.tool_id

    name = serializers.CharField()

    channel_name = serializers.SerializerMethodField()
    def get_channel_name(self, obj):
        return obj.channel_id

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        if obj.created is None:
            return None
        return datetime.fromtimestamp(obj.created, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        if obj.created is None:
            return None
        return datetime.fromtimestamp(obj.created, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

class SlackHistorySerializer(serializers.Serializer):
    message_uid = serializers.SerializerMethodField()
    def get_message_uid(self, obj):
        return f"slack-msg-{obj.id}"

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.user is None:
            return None
        return obj.user.m_developer_id

    project_id = serializers.IntegerField()
    
    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    reply_to_id = serializers.SerializerMethodField()
    def get_reply_to_id(self, obj):
        if obj.parent_user:
            try:
                reply_to = SlackHistory.objects.get(Q(user=obj.parent_user) & Q(thread_ts=obj.thread_ts))
                return reply_to.id
            except:
                return None
        else:
            return None 
    
    channel_uid = serializers.SerializerMethodField()
    def get_channel_uid(self, obj):
        return f"slack-channel-{obj.channel.id}"

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return '_'
    
    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.text

    num_reactions = serializers.IntegerField()

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        if obj.ts is None:
            return None
        return datetime.fromtimestamp(obj.ts, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        if obj.ts is None:
            return None
        return datetime.fromtimestamp(obj.ts, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

class SlackMentionSerializer(serializers.Serializer):
    mention_uid = serializers.SerializerMethodField()
    def get_mention_uid(self, obj):
        return f"slack-mention-{obj.id}"

    message_id = serializers.SerializerMethodField()
    def get_message_id(self, obj):
        return obj.message.id

    mention_to = serializers.SerializerMethodField()
    def get_mention_to(self, obj):
        return obj.mention_to.m_developer_id

    project_id = serializers.IntegerField()

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.reg_date

    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.reg_date