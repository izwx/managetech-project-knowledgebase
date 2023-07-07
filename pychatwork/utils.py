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

from django.db.models import Q
from django.conf import settings
from .models import ChatworkRoom, ChatworkMember, ChatworkMessage, ChatworkMention, ChatworkFile, ChatworkTask
from dbanalysis.models import DProjectToolInfo, DDeveloperToolMap, DTool, DChannel, DMessage, DMention, TOOL_INDICES
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from .apis import get_all_room_files, get_all_room_members, get_all_room_messages, get_all_room_tasks, get_room_info
from .serializers import ChatworkMentionSerializer, ChatworkMessageSerializer, ChatworkRoomSerializer

import re
from datetime import datetime
import pytz

def create_update_member(data: dict):
    '''
    Create a memeber if it is new, or update it if it exists.
    '''
    try:
        model_member = None
        try:
            model_member = ChatworkMember.objects.get(account_id=data['account_id'])
        except:
            model_member = ChatworkMember()
            model_member.account_id = data['account_id']

        model_member.name = data['name']
        model_member.role = data['role']
        model_member.chatwork_id = data['chatwork_id']
        model_member.organization_id = data['organization_id']
        model_member.organization_name = data['organization_name']
        model_member.department = data['department']
        model_member.avatar_image_url = data['avatar_image_url']
        model_member.department = data['department']            
        
        # developer map
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['chatwork']) & Q(account_name = data['account_id']))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_member.m_developer_id is None:
                model_member.m_developer_id = m_developer.developer_id
            if m_developer.s3_bucket_key is None:
                my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_member.avatar_image_url, create_object_key('png'))
                m_developer.s3_bucket_key = object_key
                m_developer.save()

        model_member.save()

        return model_member

    except Exception as err:
        print('CHATWORK member error')
        print(str(err))

def create_update_room(data: dict, project_id):
    '''
    Create a room if it is new, or update it if it exists.
    '''
    try:
        model_room = None
        try:
            model_room = ChatworkRoom.objects.get(room_id=data['room_id'])
        except:
            model_room = ChatworkRoom()
            model_room.room_id = data['room_id']
            model_room.created_at = data['last_update_time']
        model_room.project_id = project_id
        model_room.name = data['name']
        model_room.type = data['type']
        model_room.icon_path = data['icon_path']
        model_room.last_update_time = data['last_update_time']
        
        model_room.save()
        
        d_model_channel = None
        try:
            d_model_channel = DChannel.objects.get(Q(tool__tool_name__iexact='chatwork') & Q(channel_name=data['room_id']))
        except:
            d_model_channel = DChannel()
            d_model_channel.channel_name = data['room_id']
            d_model_channel.created_at = datetime.fromtimestamp(data['last_update_time'], pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        d_model_channel.project = DProjectToolInfo.objects.get(project_id=project_id)
        d_model_channel.tool = DTool.objects.get(tool_name__iexact='chatwork')
        d_model_channel.name = data['name']
        d_model_channel.updated_at = datetime.fromtimestamp(data['last_update_time'], pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        d_model_channel.save()

        return model_room, d_model_channel

    except Exception as err:
        print('CHATWORK room error')
        print(str(err))
        return None, None

def create_update_message(data: dict, room_model: ChatworkRoom, d_channel_model: DChannel, project_id):
    '''
    Create a message if it is new, or update it if it exists.
    '''
    try:
        model_message = None
        try:
            model_message = ChatworkMessage.objects.get(message_id=data['message_id'])
        except:
            model_message = ChatworkMessage()
            model_message.message_id = data['message_id']
        try:
            model_message.account = ChatworkMember.objects.get(account_id = data['account']['account_id'])
        except:
            pass
        model_message.project_id = project_id
        model_message.body = data['body']
        model_message.send_time = data['send_time']
        model_message.update_time = data['update_time']

        model_message.room = room_model

        # reply to
        reply_tos = re.findall('\[rp aid=([\w =-]+)\]', data['body'])
        for rpl in reply_tos:
            sub_strings = re.findall('to=([\w-]+)', rpl)
            if len(sub_strings) > 0:
                channel_and_message = re.split("-", sub_strings[0])
                model_message.reply_to_id = channel_and_message[1]

        model_message.save()

        d_model_message = None
        try:
            d_model_message = DMessage.objects.get(Q(project__project_id=project_id) & Q(channel=d_channel_model) & Q(tool_message_uid=model_message.id))
        except:
            d_model_message = DMessage()
            d_model_message.tool_message_uid = model_message.id
        if model_message.account is not None:
            d_model_message.developer = DDeveloperToolMap.objects.get(developer_id = model_message.account.m_developer_id)
        d_model_message.project = DProjectToolInfo.objects.get(project_id=project_id)
        d_model_message.channel = d_channel_model
        d_model_message.contents = data['body']
        d_model_message.created_at = data['send_time']
        d_model_message.updated_at = data['update_time']
        
        d_model_message.save()

        # mention
        mentions = re.findall("\[To:(\d+)\]", data['body'])
        for mtn in mentions:
            try:
                ChatworkMention.objects.get(Q(message=model_message) & Q(mention_to__account_id=mtn))
            except:
                try:
                    new_mention = ChatworkMention()
                    new_mention.project_id = project_id
                    new_mention.message = model_message
                    new_mention.mention_to = ChatworkMember.objects.get(account_id=mtn)
                    new_mention.save()
                except:
                    pass

            try:
                d_developer = DDeveloperToolMap.objects.get(Q(tool_id=TOOL_INDICES['chatwork']) & Q(account_name = data['account_id']))
                try:
                    DMention.objects.get(Q(message=d_model_message) & Q(mention_to=d_developer))
                except:
                    d_new_mention = DMention()
                    d_new_mention.project = DProjectToolInfo.objects.get(project_id=project_id)
                    d_new_mention.message = d_model_message
                    d_new_mention.mention_to = d_developer
                    d_new_mention.save()
            except:
                pass
        return model_message, d_model_message

    except Exception as err:
        print('CHATWORK message error')
        print(str(err))
    
def create_update_file(data: dict, room_model: ChatworkRoom):
    '''
    Create a file if it is new, or update it if it exists.
    '''
    try:
        model_file = None
        try:
            model_file = ChatworkFile.objects.get(file_id=data['file_id'])
        except:
            model_file = ChatworkFile()
            model_file.file_id = data['file_id']
            model_file.message_id = data['message_id']    
        try:
            model_file.account = ChatworkMember.objects.get(account_id = data['account']['account_id'])
        except:
            pass

        model_file.filesize = data['filesize']
        model_file.filename = data['filename']
        model_file.upload_time = data['upload_time']

        model_file.room = room_model

        model_file.save()
        return model_file

    except Exception as err:
        print('CHATWORK file error')
        print(str(err))

def create_update_task(data: dict, room_model: ChatworkRoom):
    '''
    Create a task if it is new, or update it if it exists.
    '''
    try:
        model_task = None
        try:
            model_task = ChatworkTask.objects.get(task_id=data['task_id'])
        except:
            model_task = ChatworkTask()
            model_task.task_id = data['task_id']
            model_task.message_id = data['message_id']
        try:
            model_task.account = ChatworkMember.objects.get(account_id = data['account']['account_id'])
        except:
            pass
        try:
            model_task.assigned_by_account = ChatworkMember.objects.get(account_id = data['assigned_by_account']['account_id'])
        except:
            pass
        model_task.body = data['body']
        model_task.limit_time = data['limit_time']
        model_task.status = data['status']

        model_task.room = room_model

        model_task.save()
        return model_task

    except Exception as err:
        print('CHATWORK task error')
        print(str(err))


def update_room(conf):
    '''
    Manage a selected room and its messages, members and files and tasks.
    '''
    try:
        api_data = get_room_info(conf['target'], conf['token'])
        if api_data['success']:
            rm = api_data['data']
            print(f"Room {rm['room_id']} begin")

            model_obj, d_model_obj = create_update_room(rm, conf['project_id'])
            if model_obj:
                # members
                mem_api_data = get_all_room_members(model_obj.room_id, conf['token'])
                if mem_api_data['success']:
                    member_ids = []
                    for mem in mem_api_data['data']:
                        mem_obj = create_update_member(mem)
                        if mem_obj:
                            member_ids.append(mem_obj.id)

                    model_obj.members.set(list(ChatworkMember.objects.filter(id__in=member_ids)))
                    model_obj.save()

                # messages
                msg_api_data = get_all_room_messages(model_obj.room_id, conf['token'])
                if msg_api_data['success']:
                    for msg in msg_api_data['data']:
                        create_update_message(msg, model_obj, d_model_obj, conf['project_id'])

                # files
                files_api_data = get_all_room_files(model_obj.room_id, conf['token'])
                if files_api_data['success']:
                    for fl in files_api_data['data']:
                        create_update_file(fl, model_obj)

                # tasks
                tasks_api_data = get_all_room_tasks(model_obj.room_id, conf['token'])
                if tasks_api_data['success']:
                    for tsk in tasks_api_data['data']:
                        create_update_task(tsk, model_obj)

            print(f"Room {rm['room_id']} end")

    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

def get_chatwork_channels(start_timestamp):
    '''
    Get rooms as channels serialize them to return those as an API response.
    '''
    rooms = None

    if start_timestamp is None:
        rooms = ChatworkRoom.objects.order_by('-last_update_time')
    else:
        rooms = ChatworkRoom.objects.filter(last_update_time__gte=start_timestamp).order_by('-last_update_time')
    roomSerializer = ChatworkRoomSerializer(rooms, many=True)
    
    return roomSerializer.data

def get_chatwork_messages(start_timestamp):
    '''
    Get messages and serialize them to return those as an API response.
    '''
    messages = None
    
    if start_timestamp is None:
        messages = ChatworkMessage.objects.order_by('-send_time')
    else:
        messages = ChatworkMessage.objects.filter(Q(send_time__gte=start_timestamp) | Q(update_time__gte=start_timestamp)).order_by('-send_time')
    messageSerializer = ChatworkMessageSerializer(messages, many=True)

    return messageSerializer.data

def get_chatwork_mentions(start_timestamp):
    '''
    Get mentions and serialize them to return those as an API response.
    '''
    mentions = None

    if start_timestamp is None:
        mentions = ChatworkMention.objects.order_by('-id')
    else:
        mentions = ChatworkMention.objects.filter(Q(message__send_time__gte=start_timestamp) | Q(message__update_time__gte=start_timestamp)).order_by('-id')
    mentionSerializer = ChatworkMentionSerializer(mentions, many=True)

    return mentionSerializer.data