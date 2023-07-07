from rest_framework import serializers

class JiraIssueSerializer(serializers.Serializer):
    ticket_uid = serializers.SerializerMethodField()
    def get_ticket_uid(self, obj):
        return f"jira-ticket-{obj.id}"

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.assignee is None:
            return None
        return obj.assignee.m_developer_id

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.project.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        sprints = obj.jira_sprints.all()
        if sprints.count() == 0:
            return None
        else:
            return f"jira-sprint-{sprints.first().id}"

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.summary

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return obj.self_url

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return obj.status.name
    
    difficulty = serializers.SerializerMethodField()
    def get_difficulty(self, obj):
        return '_'

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return obj.created

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return obj.updated
    
    create_date = serializers.SerializerMethodField()
    def get_create_date(self, obj):
        return obj.created

class JiraSprintSerializer(serializers.Serializer):
    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return f"jira-sprint-{obj.id}"

    name = serializers.CharField()

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        if obj.project is None:
            return None
        return obj.project.m_project_id

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return obj.startDate

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return obj.endDate

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return obj.state # future, active, closed