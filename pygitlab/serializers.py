from rest_framework import serializers

class GitlabMergeRequestSerializer(serializers.Serializer):
    pull_request_uid = serializers.SerializerMethodField()
    def get_pull_request_uid(self, obj):
        return f"gitlab-prequest-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.m_project_id
    
    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.author is None:
            return None
        return obj.author.m_developer_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    title = serializers.CharField()

    num_comments = serializers.SerializerMethodField()
    def get_num_comments(self, obj):
        return '_'

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.description
    
    create_datetime = serializers.SerializerMethodField()
    def get_create_datetime(self, obj):
        return obj.created_at

    merge_datetime = serializers.SerializerMethodField()
    def get_merge_datetime(self, obj):
        return obj.closed_at

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return obj.web_url

class GitlabPrequestReviewerSerializer(serializers.Serializer):
    pull_request_uid = serializers.SerializerMethodField()
    def get_pull_request_uid(self, obj):
        return f"gitlab-prequest-{obj['id']}"
    reviewer_id = serializers.SerializerMethodField()
    def get_reviewer_id(self, obj):
        return obj['reviewers__m_developer_id']

class GitlabWikiSerializer(serializers.Serializer):
    document_uid = serializers.SerializerMethodField()
    def get_document_uid(self, obj):
        return f"gitlab-document-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return '_'

    title = serializers.CharField()

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.content

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.reg_date
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.reg_date