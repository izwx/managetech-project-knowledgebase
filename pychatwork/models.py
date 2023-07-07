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
from django.utils import timezone

# Create your models here.
class ChatworkConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_token = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.api_token}"

class ChatworkMember(models.Model):
    account_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=16, db_index=True)
    chatwork_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    organization_id = models.IntegerField(blank=True, null=True)
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    avatar_image_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.account_id} | {self.name}"

class ChatworkRoom(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    room_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=16, db_index=True)
    icon_path = models.URLField(blank=True, null=True)
    last_update_time = models.IntegerField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    
    members = models.ManyToManyField(ChatworkMember)

    def __str__(self) -> str:
        return f"{self.room_id} | {self.name}"

class ChatworkMessage(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    message_id = models.CharField(max_length=32, unique=True)
    account = models.ForeignKey(ChatworkMember, blank=True, null=True, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    send_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(default=0)

    reply_to_id = models.BigIntegerField(blank=True, null=True)
    room = models.ForeignKey(ChatworkRoom, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.message_id

class ChatworkMention(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    message = models.ForeignKey(ChatworkMessage, on_delete=models.CASCADE)
    mention_to = models.ForeignKey(ChatworkMember, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(default=timezone.now)

class ChatworkFile(models.Model):
    file_id = models.IntegerField(unique=True)
    message_id = models.CharField(max_length=32)
    account = models.ForeignKey(ChatworkMember, blank=True, null=True, on_delete=models.CASCADE)
    filesize = models.BigIntegerField(default=0)
    filename = models.FilePathField()
    upload_time = models.IntegerField(blank=True, null=True)

    room = models.ForeignKey(ChatworkRoom, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.file_id} | {self.filename}"

class ChatworkTask(models.Model):
    task_id = models.IntegerField(unique=True)
    account = models.ForeignKey(ChatworkMember, blank=True, null=True, on_delete=models.CASCADE, related_name='task_account')
    assigned_by_account = models.ForeignKey(ChatworkMember, blank=True, null=True, on_delete=models.CASCADE, related_name='assigend_by_account')
    message_id = models.CharField(max_length=32)
    body = models.TextField(blank=True, null=True)
    limit_time = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=8, db_index=True)

    room = models.ForeignKey(ChatworkRoom, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.account:
            return f"{self.task_id} | {self.account.name}"
        else:
            return f"{self.task_id} | No member"

class MyChatworkRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    configuration = models.ForeignKey(ChatworkConfiguration, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatworkRoom, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.room.name}"
