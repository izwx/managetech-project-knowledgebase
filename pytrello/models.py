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
from dbanalysis.models import DProjectToolInfo

# Create your models here.
class TrelloConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_key = models.CharField(max_length=50)
    app_token = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.app_key}"

class TrelloUser(models.Model):
    userId = models.CharField(max_length=32, unique=True)
    username = models.CharField(max_length=100)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    fullName = models.CharField(max_length=100, blank=True, null=True)
    initials = models.CharField(max_length=10, blank=True, null=True)
    activityBlocked = models.BooleanField(default=False)
    avatarHash = models.CharField(max_length=32, blank=True, null=True)
    avatarUrl = models.URLField(blank=True, null=True)
    nonPublicAvailable = models.BooleanField(blank=True, null=True)
    memberType = models.CharField(max_length=16, blank=True, null=True, db_index=True)
    userUrl = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.username} | {self.userId}"
    

class TrelloBoard(models.Model):
    m_project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    boardId = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False)
    idOrganization = models.CharField(max_length=32, blank=True, null=True)
    boardUrl = models.URLField(blank=True, null=True)
    shortUrl = models.URLField(unique=True, blank=True, null=True)
    dateLastActivity = models.DateTimeField(blank=True, null=True)
    dateLastView = models.DateTimeField(blank=True, null=True)
    ixUpdate = models.IntegerField(blank=True, null=True)
    
    memberCreator = models.ForeignKey(TrelloUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.boardId}"

class TrelloList(models.Model):
    listId = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    closed = models.BooleanField(default=False)
    pos = models.FloatField()

    board = models.ForeignKey(TrelloBoard, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.name} | {self.listId}"

class TrelloCard(models.Model):
    cardId = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False)
    dueComplete = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    isTemplate = models.BooleanField(default=False)

    members = models.ManyToManyField(TrelloUser, related_name="trello_card_members")
    votedMembers = models.ManyToManyField(TrelloUser, related_name="trello_card_voted_members")
    
    pos = models.FloatField()
    
    shortLink = models.CharField(max_length=10, unique=True)
    shortUrl = models.URLField(unique=True)
    cardUrl = models.URLField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    dateLastActivity = models.DateTimeField(blank=True, null=True)

    board = models.ForeignKey(TrelloBoard, on_delete=models.CASCADE)
    list = models.ForeignKey(TrelloList, on_delete=models.CASCADE)

    reg_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.name} | {self.cardId}"

class TrelloAction(models.Model):
    actionId = models.CharField(max_length=32, unique=True)
    data = models.JSONField(null=True, blank=True) # jsonType
    type = models.CharField(blank=True, null=True, max_length=50)
    date = models.DateTimeField(blank=True, null=True)
    appCreator = models.ForeignKey(TrelloUser, on_delete=models.CASCADE, blank=True, null=True, related_name="trello_action_app_creator")
    memberCreator =  models.ForeignKey(TrelloUser, on_delete=models.CASCADE, blank=True, null=True, related_name="trello_action_member_creator")
    member =  models.ForeignKey(TrelloUser, on_delete=models.CASCADE, blank=True, null=True, related_name="trello_action_member")

    def __str__(self) -> str:
        return f"{self.actionId} | {self.type}"

class MyTrelloBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    configuration = models.ForeignKey(TrelloConfiguration, on_delete=models.CASCADE)
    board = models.ForeignKey(TrelloBoard, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.board.name}"
