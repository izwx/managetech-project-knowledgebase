from rest_framework import serializers

class TrelloCardSerializer(serializers.Serializer):
    ticket_uid = serializers.SerializerMethodField()
    def get_ticket_uid(self, obj):
        return f"trello-card-{obj.id}"

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.members.count() == 0:
            return None
        first_mem = obj.members.first()
        return first_mem.m_developer_id

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.board.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.name

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return obj.shortUrl

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        if obj.closed:
            return 'closed'
        if obj.dueComplete:
            return 'done'
        return 'active'
    
    difficulty = serializers.SerializerMethodField()
    def get_difficulty(self, obj):
        return '_'

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return obj.start

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        if obj.dueComplete:
            return obj.due
        return None
    
    create_date = serializers.SerializerMethodField()
    def get_create_date(self, obj):
        if obj.start is None:
            return obj.reg_date
        else:
            if obj.reg_date < obj.start:
                return obj.reg_data
            else:
                return obj.start
            