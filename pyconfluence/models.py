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

class ConfluenceUser(models.Model):
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    accountId = models.CharField(max_length=64, db_index=True)
    email = models.EmailField(db_index=True)
    publicName = models.CharField(max_length=100)
    displayName = models.CharField(max_length=100)
    profilePicture = models.URLField(blank=True, null=True)

    reg_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.email}"

    class Meta:
        unique_together = [['domain_url', 'accountId']]

class ConfluenceSpace(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    domain_url = models.URLField(db_index=True)
    spaceId = models.BigIntegerField(db_index=True)
    spaceKey = models.CharField(max_length=64, db_index=True)
    name = models.CharField(max_length=100)
    createdBy = models.ForeignKey(ConfluenceUser, on_delete=models.CASCADE)
    createdDate = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.spaceId} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'spaceId']]
    
class ConfluencePage(models.Model):
    domain_url = models.URLField(db_index=True)
    pageId = models.BigIntegerField(db_index=True)
    space = models.ForeignKey(ConfluenceSpace, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    createdUser = models.ForeignKey(ConfluenceUser, on_delete=models.CASCADE, blank=True, null=True, related_name="confluence_page_created_user")
    createdDate = models.DateTimeField()
    updatedUser = models.ForeignKey(ConfluenceUser, on_delete=models.CASCADE, blank=True, null=True, related_name="confluence_page_updated_user")
    updatedDate = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pageId} | {self.title}"

    class Meta:
        unique_together = [['domain_url', 'pageId']]

