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
from django.db.models import Q
from django.conf import settings
from .apis import get_project, get_workitems, get_iterations, get_wiki_pages, get_wiki_identifiers, get_user_avatar
from .models import AzureboardProject, AzureboardSprint, AzureboardUser, AzureboardWorkItem, AzureboardWikiPage
from .serializers import AzureboardWorkItemSerializer, AzureboardSprintSerializer, AzureboardWikiSerializer
from dbanalysis.models import DBatchLog, DDeveloperToolMap, TOOL_INDICES, DProjectToolInfo, DSprint, DTicket
from dbanalysis.s3utils import create_boto3_session, upload_s3_from_base64_string, create_object_key
from dbanalysis.utils import check_update_model_attribute

def create_update_project(conf, data):
    '''
    Create a project if it is new, or update a project if it exists.
    '''
    try:
        model_project = None
        try:
            model_project = AzureboardProject.objects.get(Q(domain_url=conf['target']) & Q(project_id=data['id']))
        except:
            model_project = AzureboardProject()
            model_project.m_project_id = conf['project_id']
            model_project.domain_url = conf['target']
            model_project.project_id = data['id']
            model_project.createTime = data['lastUpdateTime']
        model_project.name = data['name']
        model_project.description = data.get('description')
        model_project.updateTime = data['lastUpdateTime']
        model_project.save()
        return model_project
        
    except Exception as err:
        print("AZUREBOARD PROJECT ERROR")
        print(str(err))

def create_update_sprint(conf, data, prjObj):
    '''
    Create a sprint(iteration) if it is new, or update a sprint if it exists.
    '''
    try:
        model_sprint = None
        try:
            model_sprint = AzureboardSprint.objects.get(Q(domain_url=conf['target']) & Q(sprint_id=data['id']))
            check_update_model_attribute(model_sprint, 'name', data['name'], 'update_date')
            check_update_model_attribute(model_sprint, 'path', data['path'], 'update_date')
            check_update_model_attribute(model_sprint, 'startDate', data['attributes']['startDate'], 'update_date')
            check_update_model_attribute(model_sprint, 'finishDate', data['attributes']['finishDate'], 'update_date')
        except Exception as getErr:
            model_sprint = AzureboardSprint()
            model_sprint.domain_url = conf['target']
            model_sprint.project = prjObj
            model_sprint.sprint_id = data['id']
            model_sprint.name = data['name']
            model_sprint.path = data['path']
            model_sprint.startDate = data['attributes']['startDate']
            model_sprint.finishDate = data['attributes']['finishDate']
        
        model_sprint.save()

        d_model_sprint = None
        try:
            d_model_sprint = DSprint.objects.get(Q(project__project_id=prjObj.m_project_id) & Q(unique_id=str(data['id'])))
        except:
            d_model_sprint = DSprint()
            d_model_sprint.project = DProjectToolInfo.objects.get(project_id=prjObj.m_project_id)
            d_model_sprint.unique_id = data['id']

        d_model_sprint.name = data['name']
        d_model_sprint.status = '_'
        d_model_sprint.start_date = data['attributes']['startDate']
        d_model_sprint.end_date = data['attributes']['finishDate']
        d_model_sprint.save()

        return model_sprint

    except Exception as err:
        print("AZUREBOARD SPRINT ERROR")
        print(str(err))

def create_update_user(conf, data):
    '''
    Create a user if it is new, or update a user if it exists.
    '''
    try:
        model_user = None
        try:
            model_user = AzureboardUser.objects.get(Q(domain_url=conf['target']) & Q(user_id=data['id']))
            check_update_model_attribute(model_user, 'displayName', data['displayName'], 'update_date')
            check_update_model_attribute(model_user, 'uniqueName', data['uniqueName'], 'update_date')
        except:
            model_user = AzureboardUser()
            model_user.domain_url = conf['target']
            model_user.user_id = data['id']
            model_user.displayName = data['displayName']
            model_user.uniqueName = data['uniqueName']

        # if model_user.m_developer_id is None:
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['azure']) & Q(account_name = f"{conf['target']}/{data['uniqueName']}"))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_user.m_developer_id is None:
                model_user.m_developer_id = m_developer.developer_id
            if m_developer.s3_bucket_key is None:
                avatar_b64 = get_user_avatar(conf['target'], data['descriptor'], conf['token'])
                if avatar_b64 is not None:
                    model_user.avatar = "data:image/png;base64," + avatar_b64
                    my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                    object_key = upload_s3_from_base64_string(my_session, settings.AWS_STORAGE_BUCKET_NAME, avatar_b64, create_object_key('png'))
                    m_developer.s3_bucket_key = object_key
                    m_developer.save()
                    

        model_user.save()
        return model_user

    except Exception as err:
        print("BACKLOG USER ERROR")
        print(str(err))

def create_update_workitem(conf, data, prjObj):
    '''
    Create a work item if it is new, or update a work item if it exists.
    '''
    try:
        model_workitem = None
        try:
            model_workitem = AzureboardWorkItem.objects.get(Q(domain_url=conf['target']) & Q(wi_id=data['id']))
        except:
            model_workitem = AzureboardWorkItem()
            model_workitem.domain_url = conf['target']
            model_workitem.project = prjObj
            model_workitem.wi_id = data['id']
        model_workitem.title = data['fields']['System.Title']
        model_workitem.state = data['fields']['System.State']
        model_workitem.createdDate = data['fields']['System.CreatedDate']
        model_workitem.createdBy = create_update_user(conf, data['fields']['System.CreatedBy'])
        model_workitem.changedDate = data['fields']['System.ChangedDate']
        model_workitem.changedBy = create_update_user(conf, data['fields']['System.ChangedBy'])
        if data['fields'].get('System.AssignedTo') is not None:
            model_workitem.assignedTo = create_update_user(conf, data['fields']['System.AssignedTo'])
        try:
            model_workitem.iteration = AzureboardSprint.objects.get(Q(domain_url=conf['target']) & Q(project=prjObj) & Q(path=data['fields']['System.IterationPath']))
        except:
            pass
        model_workitem.save()

        d_model_ticket = None
        try:
            d_model_ticket = DTicket.objects.get(Q(project__project_id = prjObj.m_project_id) & Q(unique_id=data['id']))
        except:
            d_model_ticket = DTicket()
            d_model_ticket.project = DProjectToolInfo.objects.get(project_id = prjObj.m_project_id)
            d_model_ticket.unique_id = data['id']
        d_model_ticket.title = data['fields']['System.Title']
        d_model_ticket.url = f"{conf['target']}/{prjObj.name}/_workitems/edit/{data['id']}/"
        d_model_ticket.status = data['fields']['System.State']
        d_model_ticket.create_date = data['fields']['System.CreatedDate']
        if model_workitem.iteration is not None:
            d_model_ticket.sprint = DSprint.objects.get(Q(project_id=prjObj.m_project_id) & Q(unique_id=model_workitem.iteration.sprint_id))
        if model_workitem.assignedTo is not None:
            if model_workitem.assignedTo.m_developer_id is not None:
                d_model_ticket.developer = DDeveloperToolMap.objects.get(developer_id=model_workitem.assignedTo.m_developer_id)
        d_model_ticket.save()

        return model_workitem

    except Exception as err:
        print("AZUREBOARD WORKITEM ERROR")
        print(str(err))

def create_update_wikipage(conf, prjObj, wiki_identifier, path):
    '''
    Create a wiki document page if it is new, or update a sprint if it exists.
    '''
    page_data = get_wiki_pages(conf['target'], conf['payload'], wiki_identifier, path, conf['token'])
    if page_data is None:
        return

    try:
        model_wikipage = None
        try:
            model_wikipage = AzureboardWikiPage.objects.get(Q(domain_url=conf['target']) & Q(wiki_identifier=wiki_identifier) & Q(wiki_path=path))
            check_update_model_attribute(model_wikipage, 'wiki_path', path, 'update_date')
            check_update_model_attribute(model_wikipage, 'content', page_data['content'], 'update_date')
        except:
            model_wikipage = AzureboardWikiPage()
            model_wikipage.domain_url = conf['target']
            model_wikipage.wiki_identifier = wiki_identifier
            model_wikipage.wiki_path = path
            model_wikipage.project = prjObj
            model_wikipage.content = page_data['content']
        model_wikipage.save()
    except Exception as err:
        print("AZUREBOARD WIKI ERROR")
        print(str(err))
    
    for subpage in page_data['subPages']:
        create_update_wikipage(conf, prjObj, wiki_identifier, subpage['path'])

def update_project(conf):
    '''
    Manage a selected project and its iterations, work items and wiki document pages.
    '''
    new_batch_log = DBatchLog()
    new_batch_log.start_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.project_id = conf['project_id']
    new_batch_log.module = 'getAzureBoardProjects:AZUREBOARD'

    try:
        projectInfo = get_project(conf['target'],  conf['payload'], conf['token'])
        projectObj = create_update_project(conf, projectInfo)

        sprints = get_iterations(conf['target'], conf['payload'], conf['token'])
        for sp in sprints:
            create_update_sprint(conf, sp, projectObj)

        workitems = get_workitems(conf['target'], conf['payload'], conf['token'])
        for wi in workitems:
            create_update_workitem(conf, wi, projectObj)

        wiki_identifiers = get_wiki_identifiers(conf['target'], conf['payload'], conf['token'])
        for wk_idfr in wiki_identifiers:
            create_update_wikipage(conf, projectObj, wk_idfr['id'], "/")

        new_batch_log.batch_type = 3
        new_batch_log.content = 'Success'

    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

        new_batch_log.batch_type = 1
        new_batch_log.content = str(err)

    new_batch_log.end_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.save()

def get_azureboard_workitems(start_time):
    '''
    Get work items and serialize them to return those as an API response.
    '''
    workItems = []

    if start_time is None:
        workItems = AzureboardWorkItem.objects.order_by('-id')
    else:
        workItems = AzureboardWorkItem.objects.filter(Q(createdDate__gte=start_time) | (Q(changedDate__isnull=False) & Q(changedDate__gte=start_time))).order_by('-id')

    serializer = AzureboardWorkItemSerializer(workItems, many=True)

    return serializer.data

def get_azureboard_sprints(start_time):
    '''
    Get sprints(iterations) and serialize them to return those as an API response.
    '''
    sprints = []

    if start_time is None:
        sprints = AzureboardSprint.objects.order_by('-id')
    else:
        sprints = AzureboardSprint.objects.filter(Q(reg_date__gte=start_time) | (Q(update_date__isnull=False) & Q(update_date__gte=start_time))).order_by('-id')

    serializer = AzureboardSprintSerializer(sprints, many=True)

    return serializer.data

def get_azureboard_documents(start_time):
    '''
    Get wiki documents and serialize them to return those as an API response.
    '''
    documents = []

    if start_time is None:
        documents = AzureboardWikiPage.objects.order_by('-id')
    else:
        documents = AzureboardWikiPage.objects.filter(Q(reg_date__gte=start_time) | Q(update_date__gte=start_time)).order_by('-id')
    documentSerializer = AzureboardWikiSerializer(documents, many=True)

    return documentSerializer.data