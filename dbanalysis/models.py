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
from .tool_indices import *

# Create your models here.
class DTool(models.Model):
    tool_id = models.BigIntegerField()
    tool_name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return f"{self.tool_name}"

class DDeveloperToolMap(models.Model): # Account name and developer mapping on tools such as Jira, Charwork, redmine.
    developer_id = models.BigIntegerField()
    tool_id = models.IntegerField(choices=TOOL_INDEX_LIST)
    account_name = models.CharField(max_length=100)
    s3_bucket_key = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.account_name} | {self.developer_id} | {self.tool_id}"

class DProjectToolInfo(models.Model):
    project_id = models.BigIntegerField()
    tool_id = models.IntegerField(choices=TOOL_INDEX_LIST)
    d_tool = models.ForeignKey(DTool, on_delete=models.SET_NULL, blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    target = models.CharField(max_length=100, blank=True, null=True)
    payload = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.get_tool_id_display()} | PrjID: {self.project_id}"

BATCH_TYPES = (
    (1, 'error',),
    (2, 'warning',),
    (3, 'info',),
)

class DBatchLog(models.Model):
    project_id = models.BigIntegerField()
    module = models.CharField(max_length=64)
    batch_type = models.PositiveSmallIntegerField(choices=BATCH_TYPES)
    content = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

# messenger tools
class DChannel(models.Model):
    channel_uid = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    tool = models.ForeignKey(DTool, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    channel_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.channel_uid} | Channel"

class DMessage(models.Model):
    message_uid = models.BigAutoField(primary_key=True)
    tool_message_uid = models.BigIntegerField(db_index=True)
    developer = models.ForeignKey(DDeveloperToolMap, on_delete=models.CASCADE, )
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    channel = models.ForeignKey(DChannel, on_delete=models.CASCADE)
    reply_to_id = models.BigIntegerField(null=True, blank=True)
    contents = models.TextField(default='', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.message_uid} | Message"

class DMention(models.Model):
    mention_uid = models.BigAutoField(primary_key=True)
    message = models.ForeignKey(DMessage, on_delete=models.CASCADE)
    mention_to = models.ForeignKey(DDeveloperToolMap, on_delete=models.CASCADE)
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.mention_uid} | Mention"

class DPullRequest(models.Model):
    pull_request_uid = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    developer = models.ForeignKey(DDeveloperToolMap, on_delete=models.CASCADE, )
    title = models.CharField(max_length=100, blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    create_datetime = models.DateTimeField(default=timezone.now)
    merge_datetime = models.DateTimeField(default=timezone.now)
    url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pull_request_uid} | PRequest"

class DSprint(models.Model):
    sprint_uid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, )
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=16, default='_')

    def __str__(self) -> str:
        return f"{self.sprint_uid} | Sprint"
    
    class Meta:
        unique_together = [['project', 'unique_id']]
    
class DTicket(models.Model):
    ticket_uid = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    developer = models.ForeignKey(DDeveloperToolMap, on_delete=models.CASCADE, )
    sprint = models.ForeignKey(DSprint, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100,)
    url = models.URLField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True, db_index=True)
    difficulty = models.CharField(max_length=16, default='_')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.ticket_uid} | Ticket"
    
    class Meta:
        unique_together = [['project', 'unique_id']]
    
class DDocument(models.Model):
    document_uid = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(DProjectToolInfo, on_delete=models.CASCADE)
    sprint = models.ForeignKey(DSprint, on_delete=models.CASCADE, blank=True, null=True)
    developer = models.ForeignKey(DDeveloperToolMap, on_delete=models.CASCADE, )
    title = models.CharField(max_length=100,)
    contents = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.document_uid} | Document"
    
    class Meta:
        unique_together = [['project', 'title']]