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
class AzureboardUser(models.Model):
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    user_id = models.CharField(max_length=48, db_index=True)
    displayName = models.CharField(max_length=64)
    uniqueName = models.EmailField()
    avatar = models.TextField(blank=True, null=True)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.uniqueName}"

    class Meta:
        unique_together = [['domain_url', 'user_id']]

class AzureboardProject(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    project_id = models.CharField(max_length=48, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    createTime = models.DateTimeField()
    updateTime = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.project_id} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'project_id']]

class AzureboardSprint(models.Model):
    domain_url = models.URLField(db_index=True)
    project = models.ForeignKey(AzureboardProject, on_delete=models.CASCADE)
    sprint_id = models.CharField(max_length=48, db_index=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100, db_index=True)
    startDate = models.DateTimeField(blank=True, null=True)
    finishDate = models.DateTimeField(blank=True, null=True)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.sprint_id} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'sprint_id']]

class AzureboardWorkItem(models.Model):
    domain_url = models.URLField(db_index=True)
    project = models.ForeignKey(AzureboardProject, on_delete=models.CASCADE)
    wi_id = models.BigIntegerField(db_index=True)
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=16, blank=True, null=True)
    iteration = models.ForeignKey(AzureboardSprint, on_delete=models.CASCADE, blank=True, null=True)
    createdDate = models.DateTimeField()
    createdBy = models.ForeignKey(AzureboardUser, on_delete=models.CASCADE, blank=True, null=True, related_name='azureboard_workitem_creator')
    changedDate = models.DateTimeField()
    changedBy = models.ForeignKey(AzureboardUser, on_delete=models.CASCADE, blank=True, null=True, related_name='azureboard_workitem_changer')
    assignedTo = models.ForeignKey(AzureboardUser, on_delete=models.CASCADE, blank=True, null=True, related_name='azureboard_workitem_assign')

    def __str__(self) -> str:
        return f"{self.wi_id} | {self.title}"

    class Meta:
        unique_together = [['domain_url', 'wi_id']]

class AzureboardWikiPage(models.Model):
    domain_url = models.URLField(db_index=True)
    wiki_identifier = models.CharField(max_length=64, db_index=True)
    wiki_path = models.URLField(db_index=True)
    project = models.ForeignKey(AzureboardProject, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.wiki_identifier} | {self.wiki_path}"
