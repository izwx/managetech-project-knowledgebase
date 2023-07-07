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

# Create your models here.

class BacklogUser(models.Model):
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    backlogId = models.BigIntegerField(db_index=True)
    userId = models.CharField(max_length=16, db_index=True)
    name = models.CharField(max_length=64)
    roleType = models.PositiveSmallIntegerField()
    lang = models.CharField(max_length=4)
    mailAddress = models.EmailField(db_index=True)
    # nulab
    nulabId = models.CharField(unique=True, max_length=100, blank=True, null=True)
    uniqueId = models.CharField(unique=True, max_length=100, blank=True, null=True)

    user_icon = models.TextField(blank=True, null=True)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.mailAddress}"

    class Meta:
        unique_together = [['domain_url', 'backlogId']]

class BacklogProject(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    projectId = models.BigIntegerField(db_index=True)
    projectKey = models.CharField(max_length=64, db_index=True)
    name = models.CharField(max_length=64)
    archived = models.BooleanField(default=False)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.projectId} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'projectId']]

class BacklogVersion(models.Model):
    domain_url = models.URLField(db_index=True)
    versionId = models.BigIntegerField(db_index=True)
    project = models.ForeignKey(BacklogProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    startDate = models.DateTimeField(blank=True, null=True)
    releaseDueDate = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.versionId} | {self.name}"
    
    class Meta:
        unique_together = [['domain_url', 'versionId']]

class BacklogIssue(models.Model):
    domain_url = models.URLField(db_index=True)
    issueId = models.BigIntegerField(db_index=True)
    project = models.ForeignKey(BacklogProject, on_delete=models.CASCADE)
    issueKey = models.CharField(max_length=64, db_index=True)
    keyId = models.BigIntegerField(db_index=True)
    issueType = models.CharField(max_length=16, db_index=True)
    summary = models.CharField(max_length=64, db_index=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=16, db_index=True)
    status = models.CharField(max_length=16, db_index=True)
    assignee = models.ForeignKey(BacklogUser, on_delete=models.CASCADE, blank=True, null=True, related_name="backlog_issue_assignee")
    versions = models.ManyToManyField(BacklogVersion, blank=True, null=True, related_name='backlog_versions')
    startDate = models.DateTimeField(blank=True, null=True)
    dueDate = models.DateTimeField(blank=True, null=True)
    estimatedHours = models.IntegerField(blank=True, null=True)
    actualHours = models.IntegerField(blank=True, null=True)
    createdUser = models.ForeignKey(BacklogUser, on_delete=models.CASCADE, blank=True, null=True, related_name="backlog_issue_created_user")
    created = models.DateTimeField()
    updatedUser = models.ForeignKey(BacklogUser, on_delete=models.CASCADE, blank=True, null=True, related_name="backlog_issue_updated_user")
    updated = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.issueId} | {self.summary}"

    class Meta:
        unique_together = [['domain_url', 'issueId']]

class BacklogWiki(models.Model):
    domain_url = models.URLField(db_index=True)
    wikiId = models.BigIntegerField(db_index=True)
    project = models.ForeignKey(BacklogProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    content = models.TextField(blank=True, null=True)
    createdUser = models.ForeignKey(BacklogUser, on_delete=models.CASCADE, blank=True, null=True, related_name="backlog_wiki_created_user")
    created = models.DateTimeField()
    updatedUser = models.ForeignKey(BacklogUser, on_delete=models.CASCADE, blank=True, null=True, related_name="backlog_wiki_updated_user")
    updated = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.wikiId} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'wikiId']]