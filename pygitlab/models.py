### Project Knowledge Base for Managetech
### Copyright (C) 2023  Managetech Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

from django.db import models
from django.utils import timezone
from coreauth.models import User

# Create your models here.
class GitlabConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private_token = models.CharField(max_length=64)
    root_url = models.URLField()
    group_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)

    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return_string = f"{self.user.email}"
        if self.group_id:
            return_string += f" | Grp: {self.group_id}"
        if self.project_id:
            return_string += f" | Prj: {self.project_id}"

        return return_string

class GitlabUser(models.Model):
    user_id = models.IntegerField(db_index=True)
    username = models.CharField(max_length=64, db_index=True)
    web_url = models.URLField(unique=True, blank=True, null=True)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=16)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.user_id) + " | " + self.username


class GitlabCommit(models.Model):
    commit_id = models.CharField(max_length=64, db_index=True)
    short_id = models.CharField(max_length=10, db_index=True)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)
    authored_date = models.DateTimeField(blank=True, null=True)
    committer_name = models.CharField(max_length=100, blank=True, null=True)
    committer_email = models.EmailField(blank=True, null=True)
    committed_date = models.DateTimeField(blank=True, null=True)
    web_url = models.URLField(unique=True)

    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"Commit | {self.short_id}"

class GitlabBranch(models.Model):
    name = models.CharField(max_length=32)
    merged = models.BooleanField(blank=True, null=True)
    protected = models.BooleanField(blank=True, null=True)
    web_url = models.URLField(unique=True)
    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.web_url

class GitlabWiki(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True)
    wiki_id = models.CharField(db_index=True, max_length=100)
    format = models.CharField(max_length=24)
    slug = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=100)
    encoding = models.CharField(max_length=16, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    group_or_project = models.BooleanField(default=False)

    reg_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.wiki_id}"

class GitlabMergeRequest(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True)
    request_id = models.IntegerField(db_index=True)
    request_iid = models.IntegerField(db_index=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=16, blank=True, null=True) # opened, closed, locked, merged
    merge_user = models.ForeignKey(GitlabUser, blank=True, null=True, on_delete=models.CASCADE, related_name='merge_user')
    merged_at = models.DateTimeField(blank=True, null=True)
    closed_by = models.ForeignKey(GitlabUser, blank=True, null=True, on_delete=models.CASCADE, related_name='closed_by_user')
    closed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    target_branch = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    source_branch = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    author = models.ForeignKey(GitlabUser, blank=True, null=True, on_delete=models.CASCADE, related_name='author')
    assignee = models.ForeignKey(GitlabUser, blank=True, null=True, on_delete=models.CASCADE, related_name='assignee')
    assignees = models.ManyToManyField(GitlabUser, related_name='assignees', blank=True)
    reviewers = models.ManyToManyField(GitlabUser, related_name='reviewers', blank=True)
    draft = models.BooleanField(default=False)
    work_in_progress = models.BooleanField(default=True)
    web_url = models.URLField(unique=True)

    def __str__(self) -> str:
        return f"{self.title} | {self.web_url}"

class GitlabGroup(models.Model):
    group_id = models.IntegerField(db_index=True)
    web_url = models.URLField(unique=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=16)
    avatar_url = models.URLField(blank=True, null=True)
    full_name = models.CharField(max_length=100)
    full_path = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    members = models.ManyToManyField(GitlabUser)
    wikis = models.ManyToManyField(GitlabWiki)

    def __str__(self) -> str:
        return f"{self.group_id} | {self.full_name}"

class GitlabProject(models.Model):
    project_id = models.IntegerField(db_index=True)
    web_url = models.URLField(unique=True)
    name = models.CharField(max_length=100)
    name_with_namespace = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    path_with_namespace = models.CharField(max_length=100)
    default_branch = models.CharField(max_length=32)
    readme_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    creator = models.ForeignKey(GitlabUser, on_delete=models.CASCADE, blank=True, null=True, related_name="gitlab_project_creator")

    empty_repo = models.BooleanField(blank=True, null=True)
    archived = models.BooleanField(blank=True, null=True)
    visibility = models.CharField(max_length=16)

    created_at = models.DateTimeField()
    last_activity_at = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField(GitlabUser, related_name="gitlab_project_members")
    branches = models.ManyToManyField(GitlabBranch)
    commits = models.ManyToManyField(GitlabCommit)
    merge_requests = models.ManyToManyField(GitlabMergeRequest)

    wikis = models.ManyToManyField(GitlabWiki)

    def __str__(self) -> str:
        return f"{self.project_id} | {self.name}"
    
class MyGitlabGroupProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    configuration = models.ForeignKey(GitlabConfiguration, on_delete=models.CASCADE)
    is_group = models.BooleanField(default=False)
    is_project = models.BooleanField(default=False)
    project = models.ForeignKey(GitlabProject, blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(GitlabGroup, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.is_group:
            return f"{self.user.email} | Group: {self.group.name}"
        elif self.is_project:
            return f"{self.user.email} | Group: {self.project.name}"
        else:
            return self.user.email