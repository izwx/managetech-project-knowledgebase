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
class SlackTeam(models.Model):
    team_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    email_domain = models.CharField(max_length=100, blank=True, null=True)
    icon = models.URLField(blank=True, null=True)
    avatar_base_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.team_id} | {self.name}"

class SlackUser(models.Model):
    user_id = models.CharField(max_length=16, unique=True)
    team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    deleted = models.BooleanField(blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    tz = models.CharField(max_length=24, blank=True, null=True)

    is_admin = models.BooleanField(blank=True, null=True)
    is_owner = models.BooleanField(blank=True, null=True)
    is_primary_owner = models.BooleanField(blank=True, null=True)
    is_restricted = models.BooleanField(blank=True, null=True)
    is_ultra_restricted = models.BooleanField(blank=True, null=True)
    is_bot = models.BooleanField(blank=True, null=True)
    is_app_user = models.BooleanField(blank=True, null=True)
    is_email_confirmed = models.BooleanField(blank=True, null=True)
    
    updated = models.FloatField(blank=True, null=True)
    who_can_share_contact_card = models.CharField(max_length=32, blank=True, null=True)

    # profile
    title = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    skype = models.CharField(max_length=64, blank=True, null=True)
    display_name = models.CharField(max_length=64, blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user_id} | {self.name}"

class SlackChannel(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    channel_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    name_normalized = models.CharField(max_length=100)
    is_channel = models.BooleanField(blank=True, null=True)
    is_group = models.BooleanField(blank=True, null=True)
    is_im = models.BooleanField(blank=True, null=True)
    is_mpim = models.BooleanField(blank=True, null=True)
    is_private = models.BooleanField(blank=True, null=True)
    is_archived = models.BooleanField(blank=True, null=True)
    is_general = models.BooleanField(blank=True, null=True)
    is_shared = models.BooleanField(blank=True, null=True)
    is_org_shared = models.BooleanField(blank=True, null=True)
    is_pending_ext_shared = models.BooleanField(blank=True, null=True)
    is_ext_shared = models.BooleanField(blank=True, null=True)
    unlinked = models.IntegerField(blank=True, null=True)
    created = models.FloatField(blank=True, null=True)
    
    shared_teams = models.ManyToManyField(SlackTeam)
    members = models.ManyToManyField(SlackUser)
    
    def __str__(self) -> str:
        return f"{self.channel_id} | {self.name}"

class SlackHistory(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    type = models.CharField(max_length=32)
    subtype = models.CharField(max_length=32, blank=True, null=True)
    ts = models.FloatField()
    text = models.TextField(blank=True, null=True)
    channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE)
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, blank=True, null=True, related_name="history_user")
    inviter = models.ForeignKey(SlackUser, on_delete=models.CASCADE, blank=True, null=True, related_name="history_inviter")
    thread_ts = models.FloatField(blank=True, null=True)
    parent_user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, blank=True, null=True, related_name="history_parent_user")
    num_reactions = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"Channel: {self.channel.name} | {self.user.user_id if self.user else 'Unknown'} | {self.ts}"

class SlackMentions(models.Model):
    project_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    message = models.ForeignKey(SlackHistory, on_delete=models.CASCADE)
    mention_to = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(default=timezone.now)