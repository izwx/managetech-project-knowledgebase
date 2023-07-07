from rest_framework import serializers

class AzureboardWorkItemSerializer(serializers.Serializer):
    ticket_uid = serializers.SerializerMethodField()
    def get_ticket_uid(self, obj):
        return f"azureboard-workitem-{obj.id}"

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.assignedTo is None:
            return None
        return obj.assignedTo.m_developer_id

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.project.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        if obj.iteration is None:
            return None
        else:
            return f"azureboard-sprint-{obj.iteration.id}"

    title = serializers.CharField()

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return f"{obj.domain_url}/{obj.project.name}/_workitems/edit/{obj.wi_id}/"

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return obj.state #To Do, Doing, Done
    
    difficulty = serializers.SerializerMethodField()
    def get_difficulty(self, obj):
        return '_'

    start_date = serializers.SerializerMethodField()
    def get_start_date(self, obj):
        return '_'

    end_date = serializers.SerializerMethodField()
    def get_end_date(self, obj):
        return '_'
    
    create_date = serializers.SerializerMethodField()
    def get_create_date(self, obj):
        return obj.createdDate

class AzureboardSprintSerializer(serializers.Serializer):
    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return f"azureboard-sprint-{obj.id}"

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
        return obj.finishDate

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return  '_'

class AzureboardWikiSerializer(serializers.Serializer):
    document_uid = serializers.SerializerMethodField()
    def get_document_uid(self, obj):
        return f"azureboard-document-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.project.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return '_'

    title = serializers.SerializerMethodField()
    def get_title(self, obj):
        return obj.wiki_path

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.content

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.reg_date
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.update_date 