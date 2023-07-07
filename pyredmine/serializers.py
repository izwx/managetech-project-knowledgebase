from rest_framework import serializers

class RedmineIssueSerializer(serializers.Serializer):
    ticket_uid = serializers.SerializerMethodField()
    def get_ticket_uid(self, obj):
        return f"redmine-ticket-{obj.id}"

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
        if obj.fixed_version is None:
            return None
        return f"redmine-version-{obj.fixed_version.id}"

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.subject

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return f"{obj.domain_url}/issues/{obj.issue_id}"

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return obj.status.name
    
    difficulty = serializers.SerializerMethodField()
    def get_difficulty(self, obj):
        return obj.priority.name

    start_date = serializers.DateField()

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return obj.due_date
    
    create_date = serializers.SerializerMethodField()
    def get_create_date(self, obj):
        return obj.created_on

class RedmineVersionSerializer(serializers.Serializer):
    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return f"redmine-version-{obj.id}"

    name = serializers.CharField()

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        if obj.project is None:
            return None
        return obj.project.m_project_id

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return obj.created_on

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return obj.due_date

    status = serializers.CharField()

class RedmineWikiSerializer(serializers.Serializer):
    document_uid = serializers.SerializerMethodField()
    def get_document_uid(self, obj):
        return f"redmine-document-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.project.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return obj.author.m_developer_id

    title = serializers.CharField()

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.text

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_on
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.updated_on