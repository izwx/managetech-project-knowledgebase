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
from .utils import update_board

@shared_task
def manage_board(conf):
    update_board(conf)

@shared_task
def update_trello_data():
    print("* -- TRELLO TASK STARTED -- *")
    confs = list(DProjectToolInfo.objects.filter(tool_id=TOOL_INDICES['trello']).values())
    print("= = Begin Trello Management = =")
    print(f"{len(confs)} Trello Configurations")
    
    for conf in confs:
        manage_board.apply_async(args=[conf])

    print("= = End Trello Management = =")
    print("* -- TRELLO TASK ENDED -- *")