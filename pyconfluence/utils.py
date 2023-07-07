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

from datetime import datetime
import pytz
import json
from django.db.models import Q
from django.conf import settings
from .manager import ConfluenceManager
from .models import ConfluenceUser, ConfluenceSpace, ConfluencePage
from .serializers import ConfluencePageSerializer
from dbanalysis.models import DBatchLog, DDeveloperToolMap, DProjectToolInfo, TOOL_INDICES, DDocument
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from dbanalysis.utils import check_update_model_attribute

def create_update_user(conf, data):
    '''
    Create a user if it is new, or update it if it exists.
    '''
    try:
        model_user = None
        try:
            model_user = ConfluenceUser.objects.get(Q(domain_url=conf['target']) & Q(accountId=data['accountId']))
            check_update_model_attribute(model_user, 'email', data['email'], 'update_date')
            if data.get('publicName') is not None:
                check_update_model_attribute(model_user, 'publicName', data['publicName'], 'update_date')
            if data.get('displayName') is not None:
                check_update_model_attribute(model_user, 'displayName', data['displayName'], 'update_date')
        except:
            model_user = ConfluenceUser()
            model_user.domain_url = conf['target']
            model_user.accountId = data['accountId']
            model_user.email = data['email']
            if data.get('publicName') is not None:
                model_user.publicName = data['publicName']
            if data.get('displayName') is not None:
                model_user.displayName = data['displayName']

        # profile picture
        if data.get('profilePicture'):
            model_user.profilePicture = conf['target'] + data['profilePicture']['path']
        
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['confluence']) & Q(account_name = f"{conf['target']}/{data['accountId']}"))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_user.m_developer_id is None:
                model_user.m_developer_id = m_developer.developer_id
            if (m_developer.s3_bucket_key is None) and (model_user.profilePicture is not None):
                my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_user.profilePicture, create_object_key('png'))
                m_developer.s3_bucket_key = object_key
                m_developer.save()
        
        model_user.save()
        return model_user
            
    except Exception as err:
        print("CONFLUENCE USER ERROR")
        print(str(err))

def create_update_space(conf, data):
    '''
    Create a space if it is new, or update it if it exists.
    '''
    try:
        model_space = None
        try:
            model_space = ConfluenceSpace.objects.get(Q(domain_url=conf['target']) & Q(spaceId=data['id']))
        except:
            model_space = ConfluenceSpace()
            model_space.m_project_id = conf['project_id']
            model_space.domain_url = conf['target']
            model_space.spaceId = data['id']
            model_space.spaceKey = data['key']
        model_space.name = data['name']
        if data.get("history") is not None:
            model_space.createdBy = create_update_user(conf, data["history"]["createdBy"])
            model_space.createdDate = data["history"]["createdDate"]

        model_space.save()
        return model_space
            
    except Exception as err:
        print("CONFLUENCE SPACE ERROR")
        print(str(err))

def create_update_page(conf, data, history, spaceObj):
    '''
    Create a wiki document page if it is new, or update it if it exists.
    '''
    try:
        model_page = None
        try:
            model_page = ConfluencePage.objects.get(Q(domain_url=conf['target']) & Q(pageId=data['id']))
        except:
            model_page = ConfluencePage()
            model_page.domain_url = conf['target']
            model_page.pageId = data['id']
            model_page.space = spaceObj
        model_page.title = data['title']
        model_page.body = data['body']['view']['value']
        model_page.createdUser = create_update_user(conf, history['createdBy']) 
        model_page.createdDate = history['createdDate']
        if history.get("lastUpdated") is not None:
            model_page.updatedUser = create_update_user(conf, history['lastUpdated']['by']) 
            model_page.updatedDate = history['lastUpdated']['when']
        model_page.save()

        d_model_page = None
        try:
            d_model_page = DDocument.objects.get(Q(project__project_id=conf['project_id']) & Q(title=data['title']))
        except:
            d_model_page = DDocument()
            d_model_page.project = DProjectToolInfo.objects.get(project_id = conf['project_id'])
            d_model_page.title= data['title']
        d_model_page.contents = data['body']['view']['value']
        d_model_page.created_at = history['createdDate']
        d_model_page.updated_at = history['lastUpdated']['when']
        if model_page.createdUser.m_developer_id is not None:
            d_model_page.developer = DDeveloperToolMap.objects.get(developer_id=model_page.createdUser.m_developer_id)
        d_model_page.save()

        return model_page
            
    except Exception as err:
        print("CONFLUENCE PAGE ERROR")
        print(str(err))

def update_project(conf):
    '''
    Manage a selected project and its spaces, and wiki document pages.
    '''
    new_batch_log = DBatchLog()
    new_batch_log.start_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.project_id = conf['project_id']
    new_batch_log.module = 'getConflenceProjects:CONFLUENCE'

    try:
        payload = json.loads(conf['payload'])
        manager = ConfluenceManager( conf['target'], payload['email'], conf['token'] )
        spaceInfo = manager.get_space(payload['key'])
        spaceObj = create_update_space(conf, spaceInfo)

        pages = manager.get_pages(payload['key'])
        for pg in pages:
            page_history = manager.get_page_history(pg['id'])
            create_update_page(conf, pg, page_history, spaceObj)

        new_batch_log.batch_type = 3
        new_batch_log.content = 'Success'
    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))
        
        new_batch_log.batch_type = 1
        new_batch_log.content = str(err)
    
    new_batch_log.end_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.save()

def get_confluence_documents(start_time):
    '''
    Get wiki documents and serialize them to return those as an API response.
    '''
    documents = []

    if start_time is None:
        documents = ConfluencePage.objects.order_by('-id')
    else:
        documents = ConfluencePage.objects.filter(Q(createdDate__gte=start_time) | (Q(updatedDate__isnull=False) & Q(updatedDate__gte=start_time))).order_by('-id')
    documentSerializer = ConfluencePageSerializer(documents, many=True)

    return documentSerializer.data