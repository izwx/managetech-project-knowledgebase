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
from coreauth.models import User

# Create your models here.
class GithubConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=64)
    repository = models.CharField(max_length=255)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.repository}"

class GithubUser(models.Model):
    user_id = models.IntegerField(unique=True)
    login = models.CharField(max_length=64, blank=True, null=True)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    node_id = models.CharField(max_length=32, unique=True)
    avatar_url = models.URLField(unique=True)
    html_url = models.URLField(unique=True)
    type=models.CharField(max_length=16)
    site_admin=models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)
    company = models.CharField(max_length=64, blank=True, null=True)
    blog = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.user_id) + " | " + self.login

class GithubCommit(models.Model):
    sha = models.CharField(max_length=64, unique=True)
    html_url = models.URLField(unique=True)
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="github_commit_author")
    committer = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="github_committer")
    message = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return "Commit | " + self.sha

class GithubCommitComment(models.Model):
    comment_id = models.IntegerField(unique=True)
    html_url = models.URLField(unique=True)
    body = models.TextField()
    path = models.URLField()
    position = models.IntegerField()
    line = models.IntegerField()
    commit_id = models.CharField(max_length=64)
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.comment_id

class GithubPullRequest(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True)
    pull_request_id = models.IntegerField(unique=True)
    html_url = models.URLField(unique=True)
    issue_url = models.URLField(blank=True, null=True)
    diff_url = models.URLField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    merged_at = models.DateTimeField(blank=True, null=True)
    merge_commit_sha = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="github_pr_user", blank=True, null=True)
    assignee = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="github_pr_assignee", blank=True, null=True)
    assignees = models.ManyToManyField(GithubUser, related_name="github_pr_assignees", blank=True)
    requested_reviewers = models.ManyToManyField(GithubUser, related_name="github_pr_reviewers", blank=True)

    def __str__(self) -> str:
        return f"{self.pull_request_id}"

class GithubRepository(models.Model):
    repo_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="github_owner")
    description = models.TextField(blank=True, null=True)
    html_url = models.URLField(unique=True)
    default_branch = models.CharField(max_length=32)
    open_issues = models.IntegerField(default=0)
    open_issues_count = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    collaborators = models.ManyToManyField(GithubUser, related_name="github_collaborators")
    assignees = models.ManyToManyField(GithubUser, related_name="github_assignees")
    commits = models.ManyToManyField(GithubCommit)
    commit_comments = models.ManyToManyField(GithubCommitComment)
    pull_requests = models.ManyToManyField(GithubPullRequest)

    def __str__(self) -> str:
        return self.full_name

class MyGithubRepository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    configuration = models.ForeignKey(GithubConfiguration, on_delete=models.CASCADE)
    repository = models.ForeignKey(GithubRepository, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.repository.name}"