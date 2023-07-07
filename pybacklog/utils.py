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
from .apis import (
    get_project_info, get_issues, get_versions, get_wikis, 
)
from .models import BacklogIssue, BacklogProject, BacklogUser, BacklogVersion, BacklogWiki
from .serializers import BacklogIssueSerializer, BacklogVersionSerializer, BacklogWikiSerializer
from dbanalysis.models import DBatchLog, DDeveloperToolMap, DProjectToolInfo, TOOL_INDICES, DSprint
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from dbanalysis.utils import check_update_model_attribute

def create_update_project(conf, data):
    '''
    Create a project if it is new, or update it if it exists.
    '''
    try:
        model_project = None
        try:
            model_project = BacklogProject.objects.get(Q(domain_url=conf['target']) & Q(projectId=data['id']))
            check_update_model_attribute(model_project, 'name', data['name'], 'update_date')
            check_update_model_attribute(model_project, 'archived', data['archived'], 'update_date')
        except:
            model_project = BacklogProject()
            model_project.m_project_id = conf['project_id']
            model_project.domain_url = conf['target']
            model_project.projectId = data['id']
            model_project.projectKey = data['projectKey']
            model_project.name = data['name']
            model_project.archived = data['archived']
        
        model_project.save()
        return model_project

    except Exception as err:
        print("BACKLOG PROJECT ERROR")
        print(str(err))

def create_update_version(conf, data, prjObj):
    '''
    Create a version as sprint if it is new, or update it if it exists.
    '''
    try:
        model_version = None
        try:
            model_version = BacklogVersion.objects.get(Q(domain_url=conf['target']) & Q(versionId=data['id']))
            check_update_model_attribute(model_version, 'name', data['name'], 'update_date')
            check_update_model_attribute(model_version, 'description', data.get('description'), 'update_date')
            check_update_model_attribute(model_version, 'startDate', data.get('startDate'), 'update_date')
            check_update_model_attribute(model_version, 'releaseDueDate', data.get('releaseDueDate'), 'update_date')
            check_update_model_attribute(model_version, 'archived', data.get('archived'), 'update_date')
        except:
            model_version = BacklogVersion()
            model_version.domain_url = conf['target']
            model_version.versionId = data['id']
            model_version.project = prjObj
            model_version.name = data['name']
            model_version.description = data.get('description')
            model_version.startDate = data.get('startDate')
            model_version.releaseDueDate = data.get('releaseDueDate')
            model_version.archived = data.get('archived')
        
        model_version.save()

        d_model_sprint = None
        try:
            d_model_sprint = DSprint.objects.get(Q(project__project_id=prjObj.m_project_id) & Q(unique_id=str(data['id'])))
        except:
            d_model_sprint = DSprint()
            d_model_sprint.project = DProjectToolInfo.objects.get(project_id=prjObj.m_project_id)
            d_model_sprint.unique_id = str(data['id'])

        d_model_sprint.name = data['name']
        d_model_sprint.status = "closed" if data.get('archived') else "opened"
        d_model_sprint.start_date = data.get('startDate')
        d_model_sprint.end_date = data.get('releaseDueDate')
        d_model_sprint.save()

        return model_version

    except Exception as err:
        print("BACKLOG VERSION ERROR")
        print(str(err))

def create_update_user(conf, data):
    '''
    Create a user if it is new, or update it if it exists.
    '''
    try:
        model_user = None
        try:
            model_user = BacklogUser.objects.get(Q(domain_url=conf['target']) & Q(backlogId=data['id']))
            check_update_model_attribute(model_user, 'name', data['name'], 'update_date')
            check_update_model_attribute(model_user, 'roleType', data.get('roleType'), 'update_date')
            check_update_model_attribute(model_user, 'lang', data.get('lang'), 'update_date')
            check_update_model_attribute(model_user, 'lang', data.get('lang'), 'update_date')
            if data.get('nulabAccount') is not None:
                check_update_model_attribute(model_user, 'nulabId', data['nulabAccount']['nulabId'], 'update_date')
                check_update_model_attribute(model_user, 'uniqueId', data['nulabAccount']['uniqueId'], 'update_date')
        except:
            model_user = BacklogUser()
            model_user.domain_url = conf['target']
            model_user.backlogId = data['id']
            model_user.userId = data['userId']
            model_user.name = data['name']
            model_user.roleType = data.get('roleType')
            model_user.lang = data.get('lang')
            model_user.mailAddress = data['mailAddress']
            if data.get('nulabAccount') is not None:
                model_user.nulabId = data['nulabAccount']['nulabId']
                model_user.uniqueId = data['nulabAccount']['uniqueId']

        # 
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['backlog']) & Q(account_name = f"{conf['target']}/{data['mailAddress']}"))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_user.m_developer_id is None:
                model_user.m_developer_id = m_developer.developer_id
            if m_developer.s3_bucket_key is None:
                # user icon
                user_icon_url = f"{conf['target']}/api/v2/users/{data['id']}/icon?apiKey={conf['token']}"
                model_user.user_icon = user_icon_url
                my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, user_icon_url, create_object_key('png'))
                m_developer.s3_bucket_key = object_key
                m_developer.save()

        model_user.save()
        return model_user

    except Exception as err:
        print("BACKLOG USER ERROR")
        print(str(err))

def create_update_issue(conf, data, prjObj):
    '''
    Create an issue as a ticket if it is new, or update it if it exists.
    '''
    try:
        model_issue = None
        try:
            model_issue = BacklogIssue.objects.get(Q(domain_url=conf['target']) & Q(issueId=data['id']))
        except:
            model_issue = BacklogIssue()
            model_issue.domain_url = conf['target']
            model_issue.issueId = data['id']
            model_issue.project = prjObj
            model_issue.issueKey = data['issueKey']
            model_issue.keyId = data['keyId']
        
        model_issue.issueType = data['keyId']
        if data.get('issueType') is not None:
            model_issue.issueType = data['issueType']['name']
        model_issue.summary = data.get('summary')
        model_issue.description = data.get('description')
        if data.get('priority') is not None:
            model_issue.priority = data['priority']['name']
        if data.get('status') is not None:
            model_issue.status = data['status']['name']
        if data.get('assignee') is not None:
            model_issue.assignee = create_update_user(conf, data['assignee'])
        
        model_issue.startDate = data.get('startDate')
        model_issue.dueDate = data.get('dueDate')
        model_issue.estimatedHours = data.get('estimatedHours')
        model_issue.actualHours = data.get('actualHours')
        if data.get('createdUser') is not None:
            model_issue.createdUser = create_update_user(conf, data['createdUser'])
        model_issue.created = data.get('created')
        if data.get('updatedUser') is not None:
            model_issue.updatedUser = create_update_user(conf, data['updatedUser'])
        model_issue.updated = data.get('updated')
        model_issue.save()
        if data.get('versions') is not None:
            version_ids = []
            for vrs in data['versions']:
                version_ids.append(create_update_version(conf, vrs, prjObj).id)
            model_issue.versions.set(BacklogVersion.objects.filter(id__in=version_ids))
        model_issue.save()
        return model_issue

    except Exception as err:
        print("BACKLOG ISSUE ERROR")
        print(str(err))

def create_update_wiki(conf, data, prjObj):
    '''
    Create a wiki document if it is new, or update it if it exists.
    '''
    try:
        model_wiki = None
        try:
            model_wiki = BacklogWiki.objects.get(Q(domain_url=conf['target']) & Q(wikiId=data['id']))
        except:
            model_wiki = BacklogWiki()
            model_wiki.domain_url = conf['target']
            model_wiki.wikiId = data['id']
            model_wiki.project = prjObj

        model_wiki.name = data['name']
        model_wiki.content = data.get('content')
        if data.get('createdUser') is not None:
            model_wiki.createdUser = create_update_user(conf, data['createdUser'])
        model_wiki.created = data.get('created')
        if data.get('updatedUser') is not None:
            model_wiki.updatedUser = create_update_user(conf, data['updatedUser'])
        model_wiki.updated = data.get('updated')
        model_wiki.save()
        return model_wiki

    except Exception as err:
        print("BACKLOG WIKI ERROR")
        print(str(err))

def update_project(conf):
    '''
    Manage a selected project and its versions, issues and wiki documents.
    '''
    new_batch_log = DBatchLog()
    new_batch_log.start_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.project_id = conf['project_id']
    new_batch_log.module = 'getBacklogProjects:BACKLOG'

    try:
        projectInfo = get_project_info(conf['target'], conf['token'], conf['payload'])
        projectObj = create_update_project(conf, projectInfo)
        versions = get_versions(conf['target'], conf['token'], projectInfo['id'])
        for vsn in versions:
            create_update_version(conf, vsn, projectObj)
        
        issues = get_issues(conf['target'], conf['token'], projectInfo['id'])
        for iss in issues:
            create_update_issue(conf, iss, projectObj)

        wikis = get_wikis(conf['target'], conf['token'], projectInfo['id'])
        for wk in wikis:
            create_update_wiki(conf, wk, projectObj)

        new_batch_log.batch_type = 3
        new_batch_log.content = 'Success'

    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

        new_batch_log.batch_type = 1
        new_batch_log.content = str(err)

    new_batch_log.end_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.save()

def get_backlog_tickets(start_time):
    '''
    Get issues as tickets and serialize them to return those as an API response.
    '''
    tickets = []

    if start_time is None:
        tickets = BacklogIssue.objects.order_by('-id')
    else:
        tickets = BacklogIssue.objects.filter(Q(created__gte=start_time) | (Q(updated__isnull=False) & Q(updated__gte=start_time))).order_by('-id')

    ticketSerializer = BacklogIssueSerializer(tickets, many=True)

    return ticketSerializer.data

def get_backlog_sprints(start_time):
    '''
    Get versions as sprints and serialize them to return those as an API response.
    '''
    sprints = []

    if start_time is None:
        sprints = BacklogVersion.objects.order_by('-id')
    else:
        sprints = BacklogVersion.objects.filter(Q(reg_date__gte=start_time) | (Q(update_date__isnull=False) & Q(update_date__gte=start_time))).order_by('-id')

    sprintSerializer = BacklogVersionSerializer(sprints, many=True)

    return sprintSerializer.data 

def get_backlog_documents(start_time):
    '''
    Get wiki documents and serialize them to return those as an API response.
    '''
    documents = []

    if start_time is None:
        documents = BacklogWiki.objects.order_by('-id')
    else:
        documents = BacklogWiki.objects.filter(Q(created__gte=start_time) | (Q(updated__isnull=False) & Q(updated__gte=start_time))).order_by('-id')
    documentSerializer = BacklogWikiSerializer(documents, many=True)

    return documentSerializer.data