from rest_framework import serializers
from dbanalysis.models import DTool
from datetime import datetime
import pytz

class ChatworkRoomSerializer(serializers.Serializer):
    channel_uid = serializers.SerializerMethodField()
    def get_channel_uid(self, obj):
        return f"chatwork-channel-{obj.id}"

    project_id = serializers.IntegerField()
    
    tool_id = serializers.SerializerMethodField()
    def get_tool_id(self, obj):
        tool_info = DTool.objects.get(tool_name__iexact='chatwork')
        return tool_info.tool_id

    name = serializers.CharField()

    channel_name = serializers.SerializerMethodField()
    def get_channel_name(self, obj):
        return obj.room_id

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        if obj.created_at is None:
            return None
        datetime.fromtimestamp(obj.created_at, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        if obj.last_update_time is None:
            return None
        datetime.fromtimestamp(obj.last_update_time, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

class ChatworkMessageSerializer(serializers.Serializer):
    message_uid = serializers.SerializerMethodField()
    def get_message_uid(self, obj):
        return f"chatwork-msg-{obj.id}"

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return obj.account.m_developer_id

    project_id = serializers.IntegerField()

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    reply_to_id = serializers.IntegerField()
    
    channel_uid = serializers.SerializerMethodField()
    def get_channel_uid(self, obj):
        return f"chatwork-channel-{obj.room.id}"

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return '_'
    
    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.body

    num_reactions = serializers.SerializerMethodField()
    def get_num_reactions(self, obj):
        return '_'

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        if obj.send_time is None:
            return None
        datetime.fromtimestamp(obj.send_time, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        if obj.update_time is None:
            return None
        datetime.fromtimestamp(obj.update_time, pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

class ChatworkMentionSerializer(serializers.Serializer):
    mention_uid = serializers.SerializerMethodField()
    def get_mention_uid(self, obj):
        return f"chatwork-mention-{obj.id}"

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