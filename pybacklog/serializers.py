from rest_framework import serializers

class BacklogIssueSerializer(serializers.Serializer):
    ticket_uid = serializers.SerializerMethodField()
    def get_ticket_uid(self, obj):
        return f"backlog-ticket-{obj.id}"

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
        versions = obj.versions.all()
        if versions.count() == 0:
            return None
        else:
            return f"backlog-version-{versions.first().id}"

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.summary

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return f"{obj.domain_url}/view/{obj.issueKey}"
    
    status = serializers.CharField()
    
    difficulty = serializers.SerializerMethodField()
    def get_difficulty(self, obj):
        return obj.priority

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return obj.startDate

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return obj.dueDate
    
    create_date = serializers.SerializerMethodField()
    def get_create_date(self, obj):
        return obj.created

class BacklogVersionSerializer(serializers.Serializer):
    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return f"backlog-version-{obj.id}"

    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return obj.name

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
        return obj.releaseDueDate

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return  "closed" if obj.archived else "opened" # future, active, closed

class BacklogWikiSerializer(serializers.Serializer):
    document_uid = serializers.SerializerMethodField()
    def get_document_uid(self, obj):
        return f"backlog-document-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.project.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return obj.createdUser.m_developer_id

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.name

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.content

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.updated 