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
class RedmineConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain_url = models.URLField()
    api_access_key = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.api_access_key}"

class RedmineTracker(models.Model):
    domain_url = models.URLField()
    tracker_id = models.IntegerField()
    name = models.CharField(max_length=16)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'tracker_id']]

class RedmineStatus(models.Model):
    domain_url = models.URLField()
    status_id = models.IntegerField()
    name = models.CharField(max_length=16)
    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'status_id']]

class RedminePriority(models.Model):
    domain_url = models.URLField()
    priority_id = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"{self.name} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'priority_id']]

class RedmineProject(models.Model):
    domain_url = models.URLField()
    project_id = models.BigIntegerField()
    m_project_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=64)
    identifier = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(blank=True, null=True)
    inherit_members = models.BooleanField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'project_id'], ['domain_url', 'identifier']]

class RedmineUser(models.Model):
    domain_url = models.URLField()
    user_id = models.BigIntegerField()
    login = models.CharField(max_length=32)
    m_developer_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    admin = models.BooleanField(blank=True, null=True)
    firstname = models.CharField(max_length=32, blank=True, null=True)
    lastname = models.CharField(max_length=32, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True) 
    last_login_on = models.DateTimeField(blank=True, null=True) 
    passwd_changed_on = models.DateTimeField(blank=True, null=True) 

    def __str__(self) -> str:
        return f"{self.login} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'user_id'], ['domain_url', 'login']]

class RedmineVersion(models.Model):
    domain_url = models.URLField()
    project = models.ForeignKey(RedmineProject, on_delete=models.CASCADE, blank=True, null=True)
    version_id = models.BigIntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, db_index=True) # open, locked, closed
    due_date = models.DateField(blank=True, null=True)
    sharing = models.CharField(max_length=32, blank=True, null=True)
    wiki_page_title = models.TextField(blank=True, null=True)
    estimated_hours = models.FloatField(default=0)
    spent_hours = models.FloatField(default=0)
    
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.version_id} | {self.name}"

    class Meta:
        unique_together = [['domain_url', 'version_id']]

class RedmineIssue(models.Model):
    domain_url = models.URLField()
    issue_id = models.BigIntegerField()
    project = models.ForeignKey(RedmineProject, on_delete=models.CASCADE)
    tracker = models.ForeignKey(RedmineTracker, on_delete=models.CASCADE)
    status = models.ForeignKey(RedmineStatus, on_delete=models.CASCADE)
    priority = models.ForeignKey(RedminePriority, on_delete=models.CASCADE)
    author = models.ForeignKey(RedmineUser, on_delete=models.CASCADE, blank=True, null=True, related_name='readmine_issue_author')
    assignee = models.ForeignKey(RedmineUser, on_delete=models.CASCADE, blank=True, null=True, related_name='redmine_issue_assignee')
    subject = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    done_ratio = models.IntegerField(default=0, blank=True, null=True)
    is_private = models.BooleanField(blank=True, null=True)
    estimated_hours = models.FloatField(blank=True, null=True)
    fixed_version = models.ForeignKey(RedmineVersion, on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True) 
    closed_on = models.DateTimeField(blank=True, null=True) 

    def __str__(self) -> str:
        return f"{self.subject} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'issue_id']]

class RedmineFile(models.Model):
    domain_url = models.URLField()
    file_id = models.BigIntegerField()
    project = models.ForeignKey(RedmineProject, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    filesize = models.IntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(RedmineUser, on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    version = models.CharField(max_length=16, blank=True, null=True)
    digest = models.CharField(max_length=100, blank=True, null=True)
    downloads = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.filename} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'file_id']]

class RedmineWiki(models.Model):
    domain_url = models.URLField()
    project = models.ForeignKey(RedmineProject, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, db_index=True)
    text = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=0)
    author = models.ForeignKey(RedmineUser, on_delete=models.SET_NULL, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title} | {self.domain_url}"

    class Meta:
        unique_together = [['domain_url', 'project', 'title']]

class MyRedmineProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    configuration = models.ForeignKey(RedmineConfiguration, on_delete=models.CASCADE)
    project = models.ForeignKey(RedmineProject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} | {self.project.name}"