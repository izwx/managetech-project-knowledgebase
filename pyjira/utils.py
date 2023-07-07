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
from atlassian import Jira
from dbanalysis.models import DBatchLog, DDeveloperToolMap, DProjectToolInfo, TOOL_INDICES, DSprint, DTicket
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from .serializers import JiraIssueSerializer, JiraSprintSerializer
from .models import JiraIssue, JiraIssueComment, JiraIssueType, JiraPriority, JiraProject, JiraStatus, JiraUser, JiraBoard, JiraSprint

import json
from datetime import datetime
import pytz

def create_or_update_user(userData, domainUrl=None):
    '''
    Create a user if it is new, or update it if it exists.
    '''

    try:
        model_user = None
        try:
            model_user = JiraUser.objects.get(self_url=userData['self'])
        except:
            model_user = JiraUser()
            model_user.self_url = userData['self']
            model_user.accountId = userData['accountId']

        model_user.displayName = userData['displayName']
        model_user.active = userData['active']
        model_user.timeZone = userData.get('timeZone')
        model_user.locale = userData.get('locale')
        model_user.avatarUrl = userData['avatarUrls']['48x48']

        # developer map
        m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['jira']) & Q(account_name = f"{domainUrl}/{userData['accountId']}"))
        if m_developer_data.count() > 0:
            m_developer = m_developer_data.first()
            if model_user.m_developer_id is None:
                model_user.m_developer_id = m_developer_data.first().developer_id
            if m_developer.s3_bucket_key is None:
                my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_user.avatarUrl, create_object_key('png'))
                m_developer.s3_bucket_key = object_key
                m_developer.save()
        model_user.save()
        
        return model_user

    except Exception as err:
        print("JIRA USER ERROR")
        print(str(err))

def create_or_update_issuetype(data):
    '''
    Create a issue type if it is new, or update it if it exists.
    '''

    try:
        model_issuetype = None
        try:
            model_issuetype = JiraIssueType.objects.get(self_url=data['self'])
        except:
            model_issuetype = JiraIssueType()
            model_issuetype.self_url = data['self']
            model_issuetype.entityId = data['entityId']
            model_issuetype.type_id = data['id']
        model_issuetype.name = data['name']
        model_issuetype.description = data['description']
        model_issuetype.iconUrl = data['iconUrl']
        model_issuetype.save()

        return model_issuetype

    except Exception as err:
        print("JIRA ISSUETYPE ERROR")
        print(str(err))

def create_or_update_status(data):
    '''
    Create a status if it is new, or update it if it exists.
    '''

    try:
        model_status = None
        try:
            model_status = JiraStatus.objects.get(self_url=data['self'])
        except:
            model_status = JiraStatus()
            model_status.self_url = data['self']
            model_status.status_id = data['id']
        model_status.name = data['name']
        model_status.description = data['description']
        model_status.save()

        return model_status

    except Exception as err:
        print("JIRA STATUS ERROR")
        print(str(err))

def create_or_update_priority(data):
    '''
    Create a priority if it is new, or update it if it exists.
    '''

    try:
        model_priority = None
        try:
            model_priority = JiraPriority.objects.get(self_url=data['self'])
        except:
            model_priority = JiraPriority()
            model_priority.self_url = data['self']
            model_priority.priority_id = data['id']
        model_priority.name = data['name']
        model_priority.iconUrl = data['iconUrl']
        model_priority.save()

        return model_priority

    except Exception as err:
        print("JIRA PRIORITY ERROR")
        print(str(err))

def create_or_update_comment(data, domainUrl=None):
    '''
    Create a comment if it is new, or update it if it exists.
    '''

    try:
        model_comment = None
        try:
            model_comment = JiraIssueComment.objects.get(self_url=data['self'])
        except:
            model_comment = JiraIssueComment()
            model_comment.self_url = data['self']
            model_comment.comment_id = data['id']
        model_comment.body = data['body']
        model_comment.created = data['created']
        model_comment.updated = data['updated']
        model_comment.jsdPublic = data['jsdPublic']

        model_comment.author = create_or_update_user(data['author'], domainUrl)
        model_comment.updateAuthor = create_or_update_user(data['updateAuthor'], domainUrl=None)

        model_comment.save()

        return model_comment

    except Exception as err:
        print("JIRA COMMENT ERROR")
        print(str(err))

def create_or_update_issue(issueData, project, domainUrl=None):
    '''
    Create a issue if it is new, or update it if it exists.
    '''

    try:
        model_issue = None
        try:
            model_issue = JiraIssue.objects.get(Q(issue_id=issueData['id']) & Q(project=project))
        except:
            model_issue = JiraIssue()
            model_issue.self_url = issueData['self']
            model_issue.issue_id = issueData['id']
            model_issue.project = project
        model_issue.key = issueData['key']
        model_issue.summary = issueData['fields']['summary']
        model_issue.timespent = issueData['fields']['timespent']
        model_issue.expand = issueData['expand']
        model_issue.created = issueData['fields']['created']
        model_issue.updated = issueData['fields']['updated']

        # users
        if issueData['fields'].get('assignee'):
            model_issue.assignee = create_or_update_user(issueData['fields'].get('assignee'), domainUrl)
        else:
            model_issue.assignee  = None
        if issueData['fields'].get('creator'):
            model_issue.creator = create_or_update_user(issueData['fields'].get('creator'), domainUrl)
        else:
            model_issue.creator  = None
        if issueData['fields'].get('reporter'):
            model_issue.reporter = create_or_update_user(issueData['fields'].get('reporter'), domainUrl)
        else:
            model_issue.reporter  = None

        # foreign keys
        model_issue.issueType = create_or_update_issuetype(issueData['fields']['issuetype'])
        model_issue.status = create_or_update_status(issueData['fields']['status'])
        model_issue.priority = create_or_update_priority(issueData['fields']['priority'])
        model_issue.save()

        # comments
        if issueData['fields']['comment'].get('comments'):
            comment_ids = []
            for comment in issueData['fields']['comment'].get('comments'):
                comment_ids.append(create_or_update_comment(comment, domainUrl).id, )
            model_issue.comments.set(list(JiraIssueComment.objects.filter(id__in=comment_ids)))
        else:
            model_issue.comments.clear()
        model_issue.save()

        return model_issue

    except Exception as err:
        print("JIRA ISSUE ERROR")
        print(str(err))

def create_or_update_project(prjData, issues, m_project_id, domainUrl=None):
    '''
    Create a project if it is new, or update it if it exists.
    '''

    try:
        model_project = None
        try:
            model_project = JiraProject.objects.get(uuid=prjData['uuid'])
            model_project.m_project_id = m_project_id
        except:
            model_project = JiraProject()
            model_project.uuid = prjData['uuid']
            model_project.self_url = prjData['self']
            model_project.m_project_id = m_project_id

        model_project.project_id = prjData['id']
        model_project.key = prjData['key']
        model_project.name = prjData['name']
        model_project.description = prjData['description']
        model_project.expand = prjData['expand']
        model_project.assigneeType = prjData['assigneeType']
        model_project.projectTypeKey = prjData['projectTypeKey']
        model_project.simplified = prjData['simplified']
        model_project.style = prjData['style']
        model_project.isPrivate = prjData['isPrivate']
        model_project.avatarUrl = prjData['avatarUrls']['48x48']
        model_project.lead = create_or_update_user(prjData['lead'], domainUrl)
        model_project.save()

        issue_ids = []
        for issData in issues:
            issue_ids.append(create_or_update_issue(issData, model_project, domainUrl).id)
        # model_project.issues.set(list(JiraIssue.objects.filter(id__in=issue_ids)))
        model_project.save()

        return model_project
    except Exception as err:
        print("JIRA PROJECT ERROR")
        print(str(err))


def create_or_update_sprint(sprintData, board, issueData, project, domainUrl=None):
    '''
    Create a sprint if it is new, or update it if it exists.
    '''

    try:
        model_sprint = None
        try:
            model_sprint = JiraSprint.objects.get(self_url=sprintData['self'])
            model_sprint.project = project
        except:
            model_sprint = JiraSprint()
            model_sprint.sprint_id = sprintData['id']
            model_sprint.self_url = sprintData['self']
            model_sprint.project = project
        model_sprint.name = sprintData['name']
        model_sprint.state = sprintData['state']
        model_sprint.startDate = sprintData['startDate']
        model_sprint.endDate = sprintData['endDate']
        model_sprint.board = board
        model_sprint.goal = sprintData['goal']
        model_sprint.save()
        issue_ids = []
        for iss in issueData['issues']:
            try:
                JiraIssue.objects.get(Q(project=project) & Q(issue_id=iss['id']))
            except:
                create_or_update_issue(iss, project, domainUrl)
            issue_ids.append(iss['id'])
        model_sprint.issues.set(list(JiraIssue.objects.filter(Q(issue_id__in=issue_ids) & Q(project=project))))
        model_sprint.save()

        d_model_sprint = None
        try:
            d_model_sprint = DSprint.objects.get(Q(project__project_id=project.m_project_id) & Q(unique_id=str(sprintData['id'])))
        except:
            d_model_sprint = DSprint()
            d_model_sprint.project = DProjectToolInfo.objects.get(project_id=project.m_project_id)
            d_model_sprint.unique_id = sprintData['id']

        d_model_sprint.name = sprintData['name']
        d_model_sprint.status = sprintData['state']
        d_model_sprint.start_date = sprintData['startDate']
        d_model_sprint.end_date = sprintData['endDate']
        d_model_sprint.save()

    except Exception as err:
        print('JIRA SPRINT ERROR')
        print(str(err))

def create_or_update_board(boardData, project):
    '''
    Create a board if it is new, or update it if it exists.
    '''

    try:
        model_board = None
        try:
            model_board = JiraBoard.objects.get(self_url=boardData['self'])
        except:
            model_board = JiraBoard()
            model_board.self_url = boardData['self']
            model_board.board_id = boardData['id']
        model_board.name = boardData['name']
        model_board.type = boardData['type']
        model_board.project = project
        model_board.save()

        return model_board

    except Exception as err:
        print('JIRA BOARD ERROR')
        print(str(err))

def update_project(conf):
    '''
    Manage a selected project and its boards, sprints and issues.
    '''

    new_batch_log = DBatchLog()
    new_batch_log.start_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.project_id = conf['project_id']
    new_batch_log.module = "getJiraProjects:JIRA"
    
    try:
        payload = json.loads(conf['payload'])
        jira = Jira(
            url=conf['target'],
            username=payload['email'],
            password=conf['token'],
            cloud=True
        )

        # projects
        prj = jira.project(payload['key'])
        print(f"Project {prj['key']} begin")

        prjData = jira.project(prj['key'])
        issues = jira.get_all_project_issues(project=prj['key'])
        projectModel = create_or_update_project(prjData, issues, conf['project_id'], conf['target'])

        boards = jira.get_all_agile_boards(project_key=projectModel.key)
        for brd in boards['values']:
            boardMdl = create_or_update_board(brd, projectModel)
            try:
                sprints = jira.get_all_sprint(board_id=brd['id'])
                for spr in sprints['values']:
                    sprint_issues = jira.get_sprint_issues(sprint_id=spr['id'], start=0, limit=50)
                    create_or_update_sprint(spr, boardMdl, sprint_issues, projectModel, conf['target'])
            except Exception as sprintErr:
                print(str(sprintErr))

        print(f"Project {prj['key']} end")

        new_batch_log.batch_type = 3
        new_batch_log.content = 'Success'

    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

        new_batch_log.batch_type = 1
        new_batch_log.content = str(err)

    new_batch_log.end_datetime = datetime.now(tz=pytz.UTC)
    new_batch_log.save()

def get_jira_tickets(start_time):
    '''
    Get tickets and serialize them to return those as an API response.
    '''

    tickets = []

    if start_time is None:
        tickets = JiraIssue.objects.order_by('-id')
    else:
        tickets = JiraIssue.objects.filter(Q(created__gte=start_time) | (Q(updated__isnull=False) & Q(updated__gte=start_time))).order_by('-id')

    ticketSerializer = JiraIssueSerializer(tickets, many=True)

    return ticketSerializer.data

def get_jira_sprints(start_time):
    '''
    Get sprints and serialize them to return those as an API response.
    '''

    sprints = []

    if start_time is None:
        sprints = JiraSprint.objects.order_by('-id')
    else:
        sprints = JiraSprint.objects.filter(Q(startDate__gte=start_time) | (Q(endDate__isnull=False) & Q(endDate__gte=start_time))).order_by('-id')

    sprintSerializer = JiraSprintSerializer(sprints, many=True)

    return sprintSerializer.data 