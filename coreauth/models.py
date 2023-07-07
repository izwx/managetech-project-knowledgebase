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
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class DCompany(models.Model):
    company_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.company_name}"

USER_ROLE_TYPE = (
    (1, 'Manager',),
    (2, 'Customer',),
    (3, 'Project Manager',),
    (4, 'Developer',),
    (5, 'Managetech Admin'),
)

USER_STATUS_TYPE = (
    (0, 'Provisional',),
    (1, 'Active',),
    (-1, 'Stopped',)
)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    #custom fields
    company = models.ForeignKey(DCompany, on_delete=models.CASCADE, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_TYPE, blank=True, null=True)
    developer_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
    user_status = models.SmallIntegerField(choices=USER_STATUS_TYPE, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
