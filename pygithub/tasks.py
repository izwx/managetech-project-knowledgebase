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

from celery import shared_task
from dbanalysis.models import DProjectToolInfo, TOOL_INDICES
from .utils import update_repository

@shared_task
def manage_repository(conf):
    update_repository(conf)

@shared_task
def update_github_data():
    print("* -- GITHUB TASK STARTED -- *")
    confs = list(DProjectToolInfo.objects.filter(tool_id=TOOL_INDICES['github']).values())
    print("= = Begin Github Management = =")
    print(f"{len(confs)} Github Configurations")

    for conf in confs:
        update_repository.apply_async(args=[conf])

    print("= = End Github Management = =")
    print("* -- GITHUB TASK ENDED -- *")