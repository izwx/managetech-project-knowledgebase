from rest_framework import serializers

class ConfluencePageSerializer(serializers.Serializer):
    document_uid = serializers.SerializerMethodField()
    def get_document_uid(self, obj):
        return f"confluence-page-{obj.id}"

    project_id = serializers.SerializerMethodField()
    def get_project_id(self, obj):
        return obj.space.m_project_id

    sprint_uid = serializers.SerializerMethodField()
    def get_sprint_uid(self, obj):
        return '_'

    developer_id = serializers.SerializerMethodField()
    def get_developer_id(self, obj):
        return obj.createdUser.m_developer_id

    title = serializers.CharField()

    contents = serializers.SerializerMethodField()
    def get_contents(self, obj):
        return obj.body

    created_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.createdDate
    
    updated_at = serializers.SerializerMethodField()
    def get_updated_at(self, obj):
        return obj.updatedDate 