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
from .utils import get_tools, get_project_tool_info, get_developer_tool_map

@shared_task
def manage_tools():
    print("* -- MANAGETECH TOOLS TASK STARTED -- *")
    if get_tools():
        print("* -- -- Successfully called the API -- -- *")
    else:
        print("* -- -- Failed to call the API -- -- *")
    print("* -- MANAGETECH TOOLS TASK ENDED -- *")

@shared_task
def manage_project_tools():
    print("* -- MANAGETECH PROJECT TOOL TASK STARTED -- *")
    if get_project_tool_info() is None:
        print("* -- -- Failed to call the API -- -- *")
    else:
        print("* -- -- Successfully called the API -- -- *")
    print("* -- MANAGETECH PROJECT TOOL TASK ENDED -- *")
    
@shared_task
def manage_developer_map():
    print("* -- MANAGETECH DEVELOPER MAP TASK STARTED -- *")
    if get_developer_tool_map() is None:
        print("* -- -- Failed to call the API -- -- *")
    else:
        print("* -- -- Successfully called the API -- -- *")
    print("* -- MANAGETECH DEVELOPER MAP TASK ENDED -- *")