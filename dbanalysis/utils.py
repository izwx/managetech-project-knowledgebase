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

import requests
from django.conf import settings
from django.db.models import Q
from datetime import datetime
import pytz

from .models import DDeveloperToolMap, DProjectToolInfo, DTool, TOOL_INDICES
from .serializers import DProjectToolInfoSerializer, DDeveloperToolMapSerializer

def get_tools():
    '''
    This function is to get tool data from the managetech dashboard
    '''
    response = requests.get(f"{settings.PLATFORM_DOMAIN}/api/v1/tool_masters")
    if response.ok:
        data = response.json()
        for tl in data['tool_masters']:
            try:
                sel_tool = DTool.objects.get(tool_name=tl['tool_name'])
                sel_tool.tool_id = tl['id']
                sel_tool.save()
            except Exception as err:
                new_tool = DTool()
                new_tool.tool_id = tl['id']
                new_tool.tool_name = tl['tool_name']
                new_tool.save()

        return True
    else:
        return False

def get_project_tool_info():
    '''
    This function is to get project data from the managetech dashboard
    '''
    # update tools
    get_tools()

    # update projects
    response = requests.get(f"{settings.PLATFORM_DOMAIN}/api/v1/project_tool_infos")
    if response.ok:
        data = response.json()
        for info in data['project_tool_infos']:
            try:
                if TOOL_INDICES.get(info['tool']['tool_name'].lower()) is None:
                    pass
                else:
                    try:
                        sel_model_ins = DProjectToolInfo.objects.get(Q(project_id=info['project_id']) & Q(tool_id=TOOL_INDICES[info['tool']['tool_name'].lower()]))
                        try:
                            sel_model_ins.d_tool = DTool.objects.get(tool_id=info['tool_id'])
                        except Exception as noToolErr1:
                            print(str(noToolErr1))
                        sel_model_ins.token = info['token']
                        sel_model_ins.target = info['target']
                        sel_model_ins.payload = info['payload']
                        sel_model_ins.save()
                    except Exception as existErr:
                        str(existErr)
                        new_model_ins = DProjectToolInfo()
                        new_model_ins.project_id = info['project_id']
                        new_model_ins.tool_id = TOOL_INDICES[info['tool']['tool_name'].lower()]
                        try:
                            new_model_ins.d_tool = DTool.objects.get(tool_id=info['tool_id'])
                        except Exception as noToolErr2:
                            print(str(noToolErr2))
                        new_model_ins.token = info['token']
                        new_model_ins.target = info['target']
                        new_model_ins.payload = info['payload']
                        new_model_ins.save()
            except Exception as err:
                print(str(err))
        serializer = DProjectToolInfoSerializer(DProjectToolInfo.objects.all(), many=True)
        return serializer.data
    else:
        return None

def get_developer_tool_map():
    '''
    This function is to get developers(members) data from the managetech dashboard
    '''
    response = requests.get(f"{settings.PLATFORM_DOMAIN}/api/v1/developer_tool_maps")
    if response.ok:
        data = response.json()
        for maap in data['developer_tool_maps']:
            try:
                if TOOL_INDICES.get(maap['tool_name'].lower()) is None:
                    pass
                else:
                    try:
                        sel_model_ins = DDeveloperToolMap.objects.get(developer_id=maap['developer_id'])
                        sel_model_ins.tool_id = TOOL_INDICES[maap['tool_name'].lower()]
                        sel_model_ins.account_name = maap['account_name']
                        sel_model_ins.save()
                    except Exception as existErr:
                        str(existErr)
                        new_model_ins = DDeveloperToolMap()
                        new_model_ins.developer_id = maap['developer_id']
                        new_model_ins.tool_id = TOOL_INDICES[maap['tool_name'].lower()]
                        new_model_ins.account_name = maap['account_name']
                        new_model_ins.save()
            except Exception as err:
                print(str(err))
        serializer = DDeveloperToolMapSerializer(DDeveloperToolMap.objects.all(), many=True)
        return serializer.data
    else:
        return None
    
def check_update_model_attribute(modelObj, attributeName, attributeValue, updateAttribute=None):
    '''
    Update both selected attribute and update date attribute when value is changed.
    '''
    if getattr(modelObj, attributeName) != attributeValue:
        setattr(modelObj, attributeName, attributeValue)
        if updateAttribute is not None:
            setattr(modelObj, updateAttribute, datetime.now(tz=pytz.UTC))