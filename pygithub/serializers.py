from rest_framework import serializers

class GithubPullRequestSerializer(serializers.Serializer):
    pull_request_uid = serializers.SerializerMethodField()
    def get_pull_request_uid(self, obj):
        return f"github-prequest-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.m_project_id
    
    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        if obj.user is None:
            return None
        return obj.user.m_developer_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    title = serializers.CharField()

    num_comments = serializers.SerializerMethodField()
    def get_num_comments(self, obj):
        return '_'

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.body
    
    create_datetime = serializers.SerializerMethodField()
    def get_create_datetime(self, obj):
        return obj.created_at

    merge_datetime = serializers.SerializerMethodField()
    def get_merge_datetime(self, obj):
        return obj.merged_at  

    url = serializers.SerializerMethodField()
    def get_url(self, obj):
        return obj.html_url

class GithubPrequestReviewerSerializer(serializers.Serializer):
    pull_request_uid = serializers.SerializerMethodField()
    def get_pull_request_uid(self, obj):
        return f"github-prequest-{obj['id']}"
    reviewer_id = serializers.SerializerMethodField()
    def get_reviewer_id(self, obj):
        return obj['requested_reviewers__m_developer_id']