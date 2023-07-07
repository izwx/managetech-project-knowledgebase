from rest_framework import serializers
from .models import DProjectToolInfo, DDeveloperToolMap, DBatchLog

class DProjectToolInfoSerializer(serializers.ModelSerializer):
    tool_name = serializers.SerializerMethodField()
    def get_tool_name(self, obj):
        return obj.get_tool_id_display()

    class Meta:
        model = DProjectToolInfo
        fields = '__all__'

class DDeveloperToolMapSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    def get_id(self, obj):
        return obj.developer_id
    tool_name = serializers.SerializerMethodField()
    def get_tool_name(self, obj):
        return obj.get_tool_id_display()
    account_name = serializers.CharField()
    s3_bucket_key = serializers.CharField()

class BatchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBatchLog
        fields = '__all__'