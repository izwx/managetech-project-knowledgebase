from django.contrib import admin
from .models import GithubConfiguration, GithubUser, GithubRepository, GithubCommit, GithubCommitComment, MyGithubRepository
from .models import GithubPullRequest

# Register your models here.

@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    list_display=('user_id', 'login', 'name')

@admin.register(GithubRepository)
class GithubRepositoryAdmin(admin.ModelAdmin):
    list_display=('repo_id', 'name', 'full_name', 'owner')

@admin.register(GithubCommit)
class GithubCommitAdmin(admin.ModelAdmin):
    pass

@admin.register(GithubCommitComment)
class GithubCommitCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(GithubPullRequest)
class GithubPullRequestAdmin(admin.ModelAdmin):
    pass