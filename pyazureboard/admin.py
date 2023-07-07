from django.contrib import admin
from .models import AzureboardUser, AzureboardProject, AzureboardWorkItem, AzureboardSprint, AzureboardWikiPage

# Register your models here.
@admin.register(AzureboardUser)
class AzureboardUserAdmin(admin.ModelAdmin):
    list_display = ('m_developer_id', 'user_id', 'displayName', )

@admin.register(AzureboardProject)
class AzureboardProjectAdmin(admin.ModelAdmin):
    list_display = ('m_project_id', 'project_id', 'name',)

@admin.register(AzureboardWorkItem)
class AzureboardWorkItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'wi_id', 'title',)

@admin.register(AzureboardSprint)
class AzureboardSprintAdmin(admin.ModelAdmin):
    list_display = ('project', 'sprint_id', 'name',)

@admin.register(AzureboardWikiPage)
class AzureboardSprintAdmin(admin.ModelAdmin):
    list_display = ('project', 'wiki_identifier', 'wiki_path',)