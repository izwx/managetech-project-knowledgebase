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

# Create your models here

class JiraUser(models.Model):
    accountId = models.CharField(max_length=32)
    self_url = models.URLField(unique=True)
    # accountType = models.CharField(max_length=24)
    emailAddress = models.EmailField(blank=True, null=True)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    displayName = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    timeZone = models.CharField(max_length=16, blank=True, null=True)
    locale = models.CharField(max_length=8, blank=True, null=True)
    avatarUrl = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.accountId} | {self.displayName}"

class JiraIssueType(models.Model):
    entityId = models.CharField(max_length=48, unique=True)
    self_url = models.URLField(unique=True)
    type_id = models.IntegerField()
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    iconUrl = models.URLField(blank=True, null=True) 

    def __str__(self) -> str:
        return f"{self.entityId} | {self.name}"

class JiraStatus(models.Model):
    self_url = models.URLField(unique=True) 
    status_id = models.IntegerField()
    name = models.CharField(max_length=24)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.self_url}"

class JiraPriority(models.Model):
    self_url = models.URLField(unique=True) 
    priority_id = models.IntegerField()
    name = models.CharField(max_length=24)
    iconUrl = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.self_url}"

class JiraIssueComment(models.Model):
    self_url = models.URLField(unique=True)
    comment_id = models.IntegerField()
    body = models.TextField()
    author = models.ForeignKey(JiraUser, on_delete=models.CASCADE, related_name="jira_comment_author")
    updateAuthor = models.ForeignKey(JiraUser, on_delete=models.CASCADE, related_name="jira_comment_update_author")
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    jsdPublic = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.self_url}"

class JiraProject(models.Model):
    uuid = models.CharField(max_length=48, db_index=True)
    self_url = models.URLField(blank=True, null=True, unique=True)
    project_id = models.IntegerField()
    m_project_id = models.BigIntegerField(blank=True, null=True)
    key = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    expand = models.TextField(blank=True, null=True)
    assigneeType = models.CharField(max_length=24, blank=True, null=True)
    projectTypeKey = models.CharField(max_length=16)
    simplified = models.BooleanField(blank=True, null=True)
    style = models.CharField(max_length=32, blank=True, null=True)
    isPrivate = models.BooleanField(blank=True, null=True)
    avatarUrl = models.URLField(blank=True, null=True)
    lead = models.ForeignKey(JiraUser, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.uuid} | {self.key}"

class JiraBoard(models.Model):
    board_id = models.IntegerField()
    self_url = models.URLField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=16)
    project = models.ForeignKey(JiraProject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"${self.name} | ${self.self_url}"

class JiraIssue(models.Model):
    project = models.ForeignKey(JiraProject, on_delete=models.CASCADE, blank=True, null=True)
    self_url = models.URLField(unique=True)
    issue_id = models.IntegerField()
    key = models.CharField(max_length=64)
    
    summary = models.TextField(blank=True, null=True)

    timespent = models.IntegerField(blank=True, null=True)
    expand = models.TextField(blank=True, null=True) 

    assignee = models.ForeignKey(JiraUser, on_delete=models.CASCADE, blank=True, null=True, related_name='jira_issue_assignee')
    issueType = models.ForeignKey(JiraIssueType, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(JiraStatus, on_delete=models.CASCADE, blank=True, null=True)
    priority = models.ForeignKey(JiraPriority, on_delete=models.CASCADE, blank=True, null=True)
    
    creator = models.ForeignKey(JiraUser, on_delete=models.CASCADE, blank=True, null=True, related_name='jira_issue_creator')
    reporter = models.ForeignKey(JiraUser, on_delete=models.CASCADE, blank=True, null=True, related_name='jira_issue_reporter')
    
    created = models.DateTimeField()
    updated = models.DateTimeField()

    comments = models.ManyToManyField(JiraIssueComment)

    def __str__(self) -> str:
        return f"{self.issue_id} | {self.summary}"

class JiraSprint(models.Model):
    sprint_id = models.IntegerField()
    self_url = models.URLField(blank=True, null=True, unique=True)
    project = models.ForeignKey(JiraProject, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=16) # future, active, closed
    name = models.CharField(max_length=64)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    board = models.ForeignKey(JiraBoard, on_delete=models.CASCADE)
    goal = models.CharField(max_length=64, blank=True, null=True)

    issues = models.ManyToManyField(JiraIssue, related_name="jira_sprints")

    def __str__(self) -> str:
        return f"{self.sprint_id} | {self.state}"