from django.contrib import admin
from .models import GitlabConfiguration, GitlabUser, GitlabGroup, GitlabProject, GitlabCommit, GitlabBranch, GitlabMergeRequest, MyGitlabGroupProject
from .models import GitlabWiki

# Register your models here.
@admin.register(GitlabUser)
class GitlabUserAdmin(admin.ModelAdmin):
    list_display=('user_id', 'username', 'web_url', 'name')

@admin.register(GitlabWiki)
class GitlabWikiAdmin(admin.ModelAdmin):
    list_display=('wiki_id', 'slug', 'title')

@admin.register(GitlabProject)
class GitlabProjectAdmin(admin.ModelAdmin):
    list_display=('project_id', 'name', 'web_url')

@admin.register(GitlabCommit)
class GitlabCommitAdmin(admin.ModelAdmin):
    list_display=('commit_id', 'web_url')

@admin.register(GitlabBranch)
class GitlabBranchAdmin(admin.ModelAdmin):
    pass

@admin.register(GitlabMergeRequest)
class GitlabMergeRequestAdmin(admin.ModelAdmin):
    pass