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
from dbanalysis.models import DBatchLog, DDeveloperToolMap, TOOL_INDICES
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from .models import SlackHistory, SlackMentions, SlackTeam, SlackUser, SlackChannel
from .serializers import SlackChannelSerializer, SlackHistorySerializer, SlackMentionSerializer
from slack_sdk import WebClient

from datetime import datetime
import pytz
import re

def create_update_team(data: dict):
    '''
    Create a team if it is new, or update it if it exists.
    '''

    try:
        model_team = None
        try:
            model_team = SlackTeam.objects.get(team_id=data['id'])
        except:
            model_team = SlackTeam()
            model_team.team_id = data.get('id')
        
        model_team.name = data.get('name')
        model_team.url = data.get('url')
        model_team.domain = data.get('domain')
        model_team.email_domain = data.get('email_domain')
        model_team.icon = data['icon'].get('image_original')
        model_team.avatar_base_url = data.get('avatar_base_url')
        model_team.is_verified = data.get('is_verified')

        model_team.save()   
        return model_team 

    except Exception as err:
        print('slack team error')
        print(str(err))
        
def create_update_user(data: dict, client: WebClient):
    '''
    Create a user if it is new, or update it if it exists.
    '''

    try:
        model_user = None
        try:
            model_user = SlackUser.objects.get(user_id = data['id'])
        except:
            model_user = SlackUser()
            model_user.user_id = data.get('id')
        
          
        # team
        if data.get('team_id'):
            response = client.team_info(team=data['team_id']).data
            model_user.team = create_update_team(response['team'])
        
        model_user.name = data.get('name')
        model_user.real_name = data.get('real_name')
        model_user.deleted = data.get('deleted')
        model_user.color = data.get('color')
        model_user.tz = data.get('tz')
        model_user.is_admin = data.get('is_admin')
        model_user.is_owner = data.get('is_owner')
        model_user.is_primary_owner = data.get('is_primary_owner')
        model_user.is_restricted = data.get('is_restricted')
        model_user.is_ultra_restricted = data.get('is_ultra_restricted')
        model_user.is_bot = data.get('is_bot')
        model_user.is_app_user = data.get('is_app_user')
        model_user.is_email_confirmed = data.get('is_email_confirmed')
        model_user.updated = data.get('updated')
        model_user.who_can_share_contact_card = data.get('who_can_share_contact_card')
        model_user.title = data['profile'].get('title')
        model_user.phone = data['profile'].get('phone')
        model_user.skype = data['profile'].get('skype')
        model_user.display_name = data['profile'].get('display_name')
        model_user.image = data['profile'].get('image_512')

        # developer map
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['slack']) & Q(account_name = data['id']))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_user.m_developer_id is None:
                model_user.m_developer_id = m_developer.developer_id
            if m_developer.s3_bucket_key is None:
                my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_user.image, create_object_key('png'))
                m_developer.s3_bucket_key = object_key
                m_developer.save()

        model_user.save()
        return model_user

    except Exception as err:
        print('slack user error')
        print(str(err))

def create_update_history(data: dict, channel_id, client: WebClient, project_id):
    '''
    Create a history as a message if it is new, or update it if it exists.
    '''

    try:
        model_history = None
        try:
            model_history = SlackHistory.objects.get(Q(channel__id=channel_id) & Q(ts=data['ts']))
        except:
            model_history = SlackHistory()
            model_history.channel = SlackChannel.objects.get(channel_id=channel_id)
            model_history.ts = data.get('ts')
        
        model_history.project_id = project_id
        model_history.type = data.get('type')
        model_history.subtype = data.get('subtype')
        model_history.text = data.get('text')
        if data.get('user') is not None:
            try:
                model_history.user = SlackUser.objects.get(user_id=data.get('user'))
            except:
                user_res = client.users_info(user=data.get('user')).data
                if user_res['ok']:
                    model_history.user = create_update_user(user_res['user'], client)
        if data.get('inviter') is not None:
            try:
                model_history.inviter = SlackUser.objects.get(user_id=data.get('inviter'))
            except:
                inviter_res = client.users_info(user=data.get('inviter')).data
                if inviter_res['ok']:
                    model_history.inviter = create_update_user(inviter_res['user'], client)

        if data.get('thread_ts') is not None:
            model_history.thread_ts = data.get('thread_ts')
        if data.get('parent_user_id') is not None:
            try:
                model_history.parent_user = SlackUser.objects.get(user_id=data.get('parent_user_id'))
            except:
                parent_res = client.users_info(user=data.get('parent_user_id')).data
                if parent_res['ok']:
                    model_history.parent_user = create_update_user(parent_res['user'], client)

        if data.get('reactions') is not None:
            reaction_count = 0
            for rct in data['reactions']:
                reaction_count += rct['count']
            model_history.num_reactions = reaction_count

        model_history.save()
        
        # mentions
        mentions = re.findall("<@([a-zA-Z0-9]+)>", data['text'])
        for mtn in mentions:
            try:
                SlackMentions.objects.get(Q(message=model_history) & Q(mention_to__user_id=mtn))
            except:
                try:
                    new_mention = SlackMentions()
                    new_mention.project_id = project_id
                    new_mention.message = model_history
                    new_mention.mention_to = SlackUser.objects.get(user_id=mtn)
                    new_mention.save()
                except:
                    pass
                
        return model_history

    except Exception as err:
        print('slack history error')
        print(str(err))

def create_update_channel(data: dict, client: WebClient, project_id):
    '''
    Create a channel if it is new, or update it if it exists.
    '''

    try:
        model_channel = None
        try:
            model_channel = SlackChannel.objects.get(channel_id=data['id'])
        except:
            model_channel = SlackChannel()
            model_channel.channel_id = data.get('id')

        model_channel.project_id = project_id
        model_channel.name = data.get('name')
        model_channel.is_channel = data.get('is_channel')
        model_channel.is_group = data.get('is_group')
        model_channel.is_im = data.get('is_im')
        model_channel.is_mpim = data.get('is_mpim')
        model_channel.is_private = data.get('is_private')
        model_channel.is_archived = data.get('is_archived')
        model_channel.is_general = data.get('is_general')
        model_channel.is_shared = data.get('is_shared')
        model_channel.is_org_shared = data.get('is_org_shared')
        model_channel.is_pending_ext_shared = data.get('is_pending_ext_shared')
        model_channel.is_ext_shared = data.get('is_ext_shared')
        model_channel.name_normalized = data.get('name_normalized')
        model_channel.unlinked = data.get('unlinked')
        model_channel.created = data.get('created')

        model_channel.save()

        # many to many
        team_ids = []
        for team_id in data['shared_team_ids']:
            response = client.team_info(team=team_id).data
            team_ids.append(create_update_team(response['team']).id)
        model_channel.shared_teams.set(list(SlackTeam.objects.filter(id__in=team_ids)))

        response = client.conversations_members(channel=data['id']).data
        user_ids = []
        for user_id in response['members']:
            res = client.users_info(user=user_id).data
            user_ids.append(create_update_user(res['user'], client).id)
        model_channel.members.set(list(SlackUser.objects.filter(id__in=user_ids)))

        model_channel.save()
        return model_channel

    except Exception as err:
        print('slack channel error')
        print(str(err))


def update_slack_channels(confInfo: dict):
    '''
    Manage a selected channel and its history.
    '''

    new_batch_log = DBatchLog()
    new_batch_log.start_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.project_id = confInfo['project_id']
    new_batch_log.module = "getSlackInfo:SLACK"

    try:
        client = WebClient(token=confInfo['token'])
        channel_res = client.conversations_info(channel=confInfo['target'])
        if channel_res['ok']:
            # channel
            chn = channel_res['channel']
            print(f"Channel {chn['id']} begin")
            create_update_channel(chn, client, confInfo['project_id'])
            # history
            history_res = client.conversations_history(channel=chn['id']).data
            if history_res['ok']:
                for msg in history_res['messages']:
                        create_update_history(msg, chn['id'], client, confInfo['project_id'])
                        if msg.get('reply_count') is not None and msg.get('reply_count') > 0:
                            # replies
                            replies_res = client.conversations_replies(channel=chn['id'], ts=msg['thread_ts']).data
                            if replies_res['ok']:
                                for rpl in replies_res['messages']:
                                    create_update_history(rpl, chn['id'], client, confInfo['project_id'])

            print(f"Channel {chn['id']} end")

        new_batch_log.batch_type = 3
        new_batch_log.content = 'Success'

    except Exception as err:
        print("* -- ERROR OCCURED -- *")
        print(str(err))

        new_batch_log.batch_type = 1
        new_batch_log.content = str(err)

    new_batch_log.end_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.save()

def get_slack_channels(start_timestamp):
    '''
    Get channels and serialize them to return those as an API response.
    '''

    channels = None

    if start_timestamp is None:
        channels = SlackChannel.objects.order_by('-created')
    else:
        channels = SlackChannel.objects.filter(created__gte=start_timestamp).order_by('-created')
    channelSerializer = SlackChannelSerializer(channels, many=True)
    
    return channelSerializer.data

def get_slack_messages(start_timestamp):
    '''
    Get history as messages and serialize them to return those as an API response.
    '''

    histories = None

    if start_timestamp is None:
        histories = SlackHistory.objects.order_by('-ts')
    else:
        histories = SlackHistory.objects.filter(ts__gte=start_timestamp).order_by('-ts')
    historySerializer = SlackHistorySerializer(histories, many=True)

    return historySerializer.data

def get_slack_mentions(start_timestamp):
    '''
    Get mentions and serialize them to return those as an API response.
    '''

    mentions = None

    if start_timestamp is None:
        mentions = SlackMentions.objects.order_by('-id')
    else:
        mentions = SlackMentions.objects.filter(message__ts__gte=start_timestamp).order_by('-id')
    mentionSerializer = SlackMentionSerializer(mentions, many=True)

    return mentionSerializer.data