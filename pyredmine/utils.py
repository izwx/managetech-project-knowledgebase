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
from .models import RedmineProject, RedmineUser, RedmineTracker, RedmineStatus, RedminePriority, RedmineFile, RedmineIssue, RedmineVersion
from .models import RedmineWiki
from dbanalysis.models import DBatchLog, DDeveloperToolMap, DProjectToolInfo, TOOL_INDICES, DSprint
from .serializers import RedmineIssueSerializer, RedmineVersionSerializer, RedmineWikiSerializer
from .apis import *

def create_update_tracker(domain_url, data):
    '''
    Create a tracker if it is new, or update it if it exists.
    '''

    try:
        tracker_model = None
        try:
            tracker_model = RedmineTracker.objects.get(Q(domain_url=domain_url) & Q(tracker_id=data['id']))
        except:
            tracker_model = RedmineTracker()
            tracker_model.domain_url = domain_url
            tracker_model.tracker_id = data['id']
        tracker_model.name = data['name']
        tracker_model.description = data['description']
        tracker_model.save()

        return tracker_model

    except Exception as err:
        print('Redmine tracker error')
        print(str(err))

def create_update_status(domain_url, data):
    '''
    Create a status if it is new, or update it if it exists.
    '''

    try:
        status_model = None
        try:
            status_model = RedmineStatus.objects.get(Q(domain_url=domain_url) & Q(status_id=data['id']))
        except:
            status_model = RedmineStatus()
            status_model.domain_url = domain_url
            status_model.status_id = data['id']
        status_model.name = data['name']
        if data.get('is_closed'):
            status_model.is_closed = data['is_closed']
        status_model.save()

        return status_model

    except Exception as err:
        print('Redmine issue status error')
        print(str(err))

def create_update_user(domain_url, data):
    '''
    Create a user if it is new, or update it if it exists.
    '''

    try:
        user_model = None
        try:
            user_model = RedmineUser.objects.get(Q(domain_url=domain_url) & Q(user_id=data['id']))
        except:
            user_model = RedmineUser()
            user_model.domain_url = domain_url
            user_model.user_id = data['id']

        # developer map
        if user_model.m_developer_id is None:
            m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['redmine']) & Q(account_name = f"{domain_url}/{data['login']}"))
            if m_developer_data.count() > 0:
                user_model.m_developer_id = m_developer_data.first().developer_id

        user_model.login = data['login']
        user_model.admin = data.get('admin')
        user_model.firstname = data.get('firstname')
        user_model.lastname = data.get('lastname')
        user_model.mail = data.get('mail')
        user_model.created_on = data.get('created_on')
        user_model.updated_on = data.get('updated_on')
        user_model.last_login_on = data.get('last_login_on')
        user_model.passwd_changed_on = data.get('passwd_changed_on')
        user_model.save()

        return user_model

    except Exception as err:
        print('Redmine user error')
        print(str(err))

def create_update_project(domain_url, data, m_project_id):
    '''
    Create a project if it is new, or update it if it exists.
    '''

    try:
        project_model = None
        try:
            project_model = RedmineProject.objects.get(Q(domain_url=domain_url) & Q(project_id=data['id']))
            project_model.m_project_id = m_project_id
        except:
            project_model = RedmineProject()
            project_model.domain_url = domain_url
            project_model.project_id = data['id']
            project_model.m_project_id = m_project_id
        project_model.name = data['name']
        project_model.identifier = data['identifier']
        project_model.description = data.get('description')
        project_model.status = data.get('status')
        project_model.is_public = data.get('is_public')
        project_model.inherit_members = data.get('inherit_members')
        project_model.created_on = data.get('created_on')
        project_model.updated_on = data.get('updated_on')
        project_model.save()

        return project_model
        
    except Exception as err:
        print("Redmine project error")
        print(str(err))

def create_update_file(domain_url, project, data):
    '''
    Create a file if it is new, or update it if it exists.
    '''

    try:
        file_model = None
        try:
            file_model = RedmineFile.objects.get(Q(domain_url=domain_url) & Q(file_id=data['id']))
        except:
            file_model = RedmineFile()
            file_model.domain_url = domain_url
            file_model.file_id = data['id']
            file_model.project = project
        file_model.filename = data.get('filename')
        file_model.filesize = data.get('filesize')
        file_model.content_type = data.get('content_type')
        file_model.description = data.get('description')
        file_model.content_url = data.get('content_url')
        file_model.thumbnail_url = data.get('thumbnail_url')
        if data.get('author'):
            file_model.author = RedmineUser.objects.get(Q(domain_url=domain_url) & Q(user_id=data['author']['id']))
        file_model.created_on = data.get('created_on')
        if data.get('version'):
            file_model.version = data['version']['name']
        file_model.digest = data.get('digest')
        if data.get('downloads') is not None:
            file_model.downloads = data['downloads']
        file_model.save()

        return file_model
        
    except Exception as err:
        print("Redmine file error")
        print(str(err))

def create_or_update_priority(domain_url, data):
    '''
    Create a priority if it is new, or update it if it exists.
    '''

    try:
        priority_model = None
        try:
            priority_model = RedminePriority.objects.get(Q(domain_url=domain_url) & Q(priority_id=data['id']))
        except:
            priority_model = RedminePriority()
            priority_model.domain_url = domain_url
            priority_model.priority_id = data['id']
        priority_model.name = data['name']
        priority_model.save()

        return priority_model

    except Exception as err:
        print("Redmine priority error")
        print(str(err))

def create_update_issue(domain_url, data):
    '''
    Create a issue if it is new, or update it if it exists.
    '''

    try:
        issue_model = None
        try:
            issue_model = RedmineIssue.objects.get(Q(domain_url=domain_url) & Q(issue_id=data['id']))
        except:
            issue_model = RedmineIssue()
            issue_model.domain_url = domain_url
            issue_model.issue_id = data['id']

        if data.get('project'):
            issue_model.project = RedmineProject.objects.get(Q(domain_url=domain_url) & Q(project_id=data['project']['id']))
        if data.get('tracker'):
            issue_model.tracker = RedmineTracker.objects.get(Q(domain_url=domain_url) & Q(tracker_id=data['tracker']['id']))
        if data.get('status'):
            issue_model.status = RedmineStatus.objects.get(Q(domain_url=domain_url) & Q(status_id=data['status']['id']))
        if data.get('priority'):
            issue_model.priority = create_or_update_priority(domain_url, data['priority'])
        if data.get('author'):
            issue_model.author = RedmineUser.objects.get(Q(domain_url=domain_url) & Q(user_id=data['author']['id']))
        if data.get('assigned_to'):
            issue_model.assignee = RedmineUser.objects.get(Q(domain_url=domain_url) & Q(user_id=data['assigned_to']['id']))
        if data.get('fixed_version'):
            issue_model.fixed_version = RedmineVersion.objects.get(Q(domain_url=domain_url) & Q(version_id=data['fixed_version']['id']))
        issue_model.subject = data.get('subject')
        issue_model.description = data.get('description')
        issue_model.start_date = data.get('start_date')
        issue_model.due_date = data.get('due_date')
        if data.get('done_ratio'):
            issue_model.done_ratio = data.get('done_ratio')
        issue_model.is_private = data.get('is_private')
        issue_model.estimated_hours = data.get('estimated_hours')
        issue_model.created_on = data.get('created_on')
        issue_model.updated_on = data.get('updated_on')
        issue_model.closed_on = data.get('closed_on')
        issue_model.save()

        return issue_model

    except Exception as err:
        print("Redmine issue error")
        print(str(err))

def create_update_wiki(domain_url, project, data):
    '''
    Create a wiki document if it is new, or update it if it exists.
    '''

    try:
        wiki_model = None
        try:
            wiki_model = RedmineWiki.objects.get(Q(domain_url=domain_url) & Q(title=data['title']))
        except:
            wiki_model = RedmineWiki()
            wiki_model.domain_url = domain_url
            wiki_model.title = data['title']
        wiki_model.project = project
        wiki_model.text = data['text']
        wiki_model.version = data['version']
        wiki_model.author = RedmineUser.objects.get(Q(domain_url=domain_url) & Q(user_id=data['author']['id']))
        wiki_model.created_on = data['created_on']
        wiki_model.updated_on = data['updated_on']

        if data.get('parent') is not None:
            wiki_model.parent = RedmineWiki.objects.get(Q(domain_url=domain_url) & Q(title=data['parent']['title']))

        wiki_model.save()

    except Exception as err:
        print("Redmine wiki error")
        print(str(err))

def create_update_version(domain_url, project, data):
    '''
    Create a version as a sprint if it is new, or update it if it exists.
    '''

    try:
        version_model = None
        try:
            version_model = RedmineVersion.objects.get(Q(domain_url=domain_url) & Q(version_id=data['id']))
        except:
            version_model = RedmineVersion()
            version_model.domain_url = domain_url
            version_model.version_id = data['id']
        version_model.project = project
        version_model.name = data['name']
        version_model.description = data['description']
        version_model.status = data['status']
        version_model.due_date = data['due_date']
        version_model.sharing = data['sharing']
        version_model.wiki_page_title = data['wiki_page_title']
        version_model.estimated_hours = data['estimated_hours']
        version_model.spent_hours = data['spent_hours']
        version_model.created_on = data['created_on']
        version_model.updated_on = data['updated_on']

        version_model.save()

        d_model_sprint = None
        try:
            d_model_sprint = DSprint.objects.get(Q(project__project_id=project.m_project_id) & Q(unique_id=str(data['id'])))
        except:
            d_model_sprint = DSprint()
            d_model_sprint.project = DProjectToolInfo.objects.get(project_id=project.m_project_id)
            d_model_sprint.unique_id = str(data['id'])

        d_model_sprint.name = data['name']
        d_model_sprint.status = data['status']
        d_model_sprint.start_date = data.get('created_on')
        d_model_sprint.end_date = data.get('due_date')
        d_model_sprint.save()

    except Exception as err:
        print("Redmine wiki error")
        print(str(err))

def update_project(confInfo: dict):
    '''
    Manage a selected project and its trackers, statuses, users, issues, versions and wiki document pages.
    '''

    conf = {
        'domain_url': confInfo['target'],
        'api_access_key': confInfo['token'],
        'project_id': confInfo['payload'],
        'm_project_id': confInfo['project_id'],
    }
    try:
        # trackers
        tracker_data = get_redmine_trackers(conf['domain_url'], conf['api_access_key'])
        if tracker_data['success']:
            for trk in tracker_data['data']['trackers']:
                create_update_tracker(conf['domain_url'], trk)

        # statuses
        status_data = get_redmine_statuses(conf['domain_url'], conf['api_access_key'])
        if status_data['success']:
            for sts in status_data['data']['issue_statuses']:
                create_update_status(conf['domain_url'], sts)

        # users
        user_data = get_redmine_users(conf['domain_url'], conf['api_access_key'])
        if user_data['success']:
            for usr in user_data['data']['users']:
                create_update_user(conf['domain_url'], usr)

        # projects
        project_data = get_redmine_project(conf['domain_url'], conf['api_access_key'], conf['project_id'])
        if project_data['success']:
            print(f"Project {project_data['data']['project']['id']} | {conf['domain_url']} begin")
            prj_obj = create_update_project(conf['domain_url'], project_data['data']['project'], conf['m_project_id'])
            file_data = get_redmine_project_files(conf['domain_url'], project_data['data']['project']['id'], conf['api_access_key'])
            if file_data['success']:
                for fl in file_data['data']['files']:
                    create_update_file(conf['domain_url'], prj_obj, fl)
            
            # wiki
            print(f"-- Project {project_data['data']['project']['id']} | {conf['domain_url']} Wiki --")
            wikis_data = get_redmine_wikis(conf['domain_url'], prj_obj.identifier, conf['api_access_key'])
            if wikis_data['success']:
                for wk in wikis_data['data']['wiki_pages']:
                    wiki_info = get_redmine_wiki(conf['domain_url'], prj_obj.identifier, wk['title'], conf['api_access_key'])
                    if wiki_info['success']:
                        create_update_wiki(conf['domain_url'], prj_obj, wiki_info['data']['wiki_page'])

            # version
            print(f"-- Project {project_data['data']['project']['id']} | {conf['domain_url']} Version --")
            versions_data = get_redmine_versions(conf['domain_url'], prj_obj.identifier, conf['api_access_key'])
            if versions_data['success']:
                for vsn in versions_data['data']['versions']:
                    version_info = get_redmine_version(conf['domain_url'], vsn['id'], conf['api_access_key'])
                    if version_info['success']:
                        create_update_version(conf['domain_url'], prj_obj, version_info['data']['version'])

            print(f"Project {project_data['data']['project']['id']} | {conf['domain_url']} end")

        # issues
        issue_data = get_redmine_issues(conf['domain_url'], conf['api_access_key'])
        if issue_data['success']:
            for isu in issue_data['data']['issues']:
                create_update_issue(conf['domain_url'], isu)
        
    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

def get_redmine_documents(start_time):
    '''
    Get wiki documents and serialize them to return those as an API response.
    '''

    documents = []

    if start_time is None:
        documents = RedmineWiki.objects.order_by('-id')
    else:
        documents = RedmineWiki.objects.filter(reg_date__gte=start_time).order_by('-id')
    documentSerializer = RedmineWikiSerializer(documents, many=True)

    return documentSerializer.data

def get_redmine_tickets(start_time):
    '''
    Get issues as tickets and serialize them to return those as an API response.
    '''

    tickets = []

    if start_time is None:
        tickets = RedmineIssue.objects.order_by('-id')
    else:
        tickets = RedmineIssue.objects.filter(Q(created_on__gte=start_time) | (Q(updated_on__isnull=False) & Q(updated_on__gte=start_time)) | (Q(closed_on__isnull=False) & Q(closed_on__gte=start_time))).order_by('-id')

    ticketSerializer = RedmineIssueSerializer(tickets, many=True)

    return ticketSerializer.data

def get_redmine_sprints(start_time):
    '''
    Get versions as sprints and serialize them to return those as an API response.
    '''

    sprints = []

    if start_time is None:
        sprints = RedmineVersion.objects.order_by('-id')
    else:
        sprints = RedmineVersion.objects.filter(Q(created_on__gte=start_time) | (Q(updated_on__isnull=False) & Q(updated_on__gte=start_time))).order_by('-id')

    sprintSerializer = RedmineVersionSerializer(sprints, many=True)

    return sprintSerializer.data 