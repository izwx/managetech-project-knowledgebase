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

from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import permissions, status

from .models import DBatchLog, DDeveloperToolMap
from .utils import get_project_tool_info, get_developer_tool_map, get_tools
from .functions import get_unix_timestamp
from .serializers import BatchLogSerializer, DDeveloperToolMapSerializer
from pyjira.utils import get_jira_sprints, get_jira_tickets
from pychatwork.utils import get_chatwork_channels, get_chatwork_messages, get_chatwork_mentions
from pyslack.utils import get_slack_messages, get_slack_channels, get_slack_mentions
from pygitlab.utils import get_gitlab_documents, get_gitlab_pull_requests, get_gitlab_prequest_reviewers
from pyredmine.utils import get_redmine_sprints, get_redmine_tickets, get_redmine_documents
from pygithub.utils import get_github_pull_requests, get_github_prequest_reviewers
from pybacklog.utils import get_backlog_documents, get_backlog_tickets, get_backlog_sprints
from pyconfluence.utils import get_confluence_documents
from pyazureboard.utils import get_azureboard_workitems, get_azureboard_sprints, get_azureboard_documents
from pytrello.utils import get_trello_cards

# Create your views here.
class TicketView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        # jira
        jira_data = get_jira_tickets(start_date)
        # redmine
        redmine_data = get_redmine_tickets(start_date)
        # backlog
        backlog_data = get_backlog_tickets(start_date)
        # azureboard
        azureboard_data = get_azureboard_workitems(start_date)
        # trello
        trello_data = get_trello_cards(start_date)
        return Response({
            'tickets': jira_data + redmine_data + backlog_data + azureboard_data + trello_data
        })

class SprintView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        # jira
        jira_data = get_jira_sprints(start_date)
        # redmine
        redmine_data = get_redmine_sprints(start_date)
        # backlog
        backlog_data = get_backlog_sprints(start_date)
        # azureboard
        azureboard_data = get_azureboard_sprints(start_date)
        return Response({
            'sprints': jira_data + redmine_data + backlog_data + azureboard_data
        })

class ChannelView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        start_date_timestamp = get_unix_timestamp(start_date)
        # slack
        slack_data = get_slack_channels(start_date_timestamp)
        # chatwork
        chatwork_data = get_chatwork_channels(start_date_timestamp)

        return Response({
            'channels': slack_data + chatwork_data,
        })

class MessageView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        start_date_timestamp = get_unix_timestamp(start_date)
        # slack
        slack_data = get_slack_messages(start_date_timestamp)
        # chatwork
        chatwork_data = get_chatwork_messages(start_date_timestamp)

        return Response({
            'messages': slack_data + chatwork_data,
        })

class MentionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        start_date_timestamp = get_unix_timestamp(start_date)
        # slack
        slack_data = get_slack_mentions(start_date_timestamp)
        # chatwork
        chatwork_data = get_chatwork_mentions(start_date_timestamp)

        return Response({
            'mentions': slack_data + chatwork_data,
        })


class DocumentView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        # gitlab
        gitlab_data = get_gitlab_documents(start_date)
        # redmine
        redmine_data = get_redmine_documents(start_date)
        # backlog
        backlog_data = get_backlog_documents(start_date)
        # confluence
        confluence_data = get_confluence_documents(start_date)
        # azureboard
        azureboard_data = get_azureboard_documents(start_date)
        return Response({
            'documents': gitlab_data + redmine_data + backlog_data + confluence_data + azureboard_data
        })

class PullRequestsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        # github
        github_data = get_github_pull_requests(start_date)
        # gitlab
        gitlab_data = get_gitlab_pull_requests(start_date)

        return Response({
            'pull_requests': github_data + gitlab_data
        })

class PullRequestReviewersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        # github
        github_data = get_github_prequest_reviewers(start_date)
        # gitlab
        gitlab_data = get_gitlab_prequest_reviewers(start_date)

        return Response({
            'prequest_reviewers': github_data + gitlab_data
        })

class BatchLogView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        batch_logs = DBatchLog.objects.order_by('-start_datetime')
        serializer = BatchLogSerializer(batch_logs, many=True)

        return Response({
            'batch_logs': serializer.data
        })

class DevelopersView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request):
        developers = DDeveloperToolMap.objects.order_by('developer_id')
        serializer = DDeveloperToolMapSerializer(developers, many=True)

        return Response({
            'developers': serializer.data
        })
