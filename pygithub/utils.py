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

from github import Github

from .models import GithubRepository, GithubUser, GithubCommit, GithubCommitComment, GithubPullRequest
from .serializers import GithubPullRequestSerializer, GithubPrequestReviewerSerializer
from dbanalysis.models import DProjectToolInfo, DDeveloperToolMap, TOOL_INDICES, DPullRequest
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from django.db.models import Q, Count
from django.conf import settings

def create_or_update_user(userObj):
    '''
    Create a user if it is new, or update it if it exists.
    '''
    model_cuser = None
    try:
        model_cuser = GithubUser.objects.get(user_id=userObj.id)
    except:
        model_cuser = GithubUser()
    model_cuser.user_id = userObj.id
    model_cuser.login = userObj.login
    model_cuser.node_id = userObj.node_id
    model_cuser.avatar_url = userObj.avatar_url
    model_cuser.html_url = userObj.html_url

    model_cuser.type = userObj.type
    model_cuser.site_admin = userObj.site_admin
    model_cuser.name = userObj.name
    model_cuser.company = userObj.company
    model_cuser.blog = userObj.blog
    model_cuser.location = userObj.location
    model_cuser.email = userObj.email
    model_cuser.bio = userObj.bio
    model_cuser.created_at = userObj.created_at
    model_cuser.updated_at = userObj.updated_at
    
    # developer map
    m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['github']) & Q(account_name = userObj.html_url))
    if m_developer_data.count() > 0:
        m_developer = m_developer_data.first()
        if model_cuser.m_developer_id is None:
            model_cuser.m_developer_id = m_developer.developer_id
        if m_developer.s3_bucket_key is None:
            my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
            object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_cuser.avatar_url, create_object_key('png'))
            m_developer.s3_bucket_key = object_key
            m_developer.save()
    
    model_cuser.save()

    return model_cuser

def create_or_update_commit(commitObj):
    '''
    Create a commit if it is new, or update it if it exists.
    '''
    model_cmt = None
    try:
        model_cmt = GithubCommit.objects.get(sha=commitObj.sha)
    except:
        model_cmt = GithubCommit()
    model_cmt.sha = commitObj.sha
    model_cmt.html_url = commitObj.commit.html_url
    model_cmt.author = create_or_update_user(commitObj.author)
    model_cmt.committer = create_or_update_user(commitObj.committer)
    model_cmt.message = commitObj.commit.message
    model_cmt.save()
    
    return model_cmt

def create_or_update_comment(commentObj):
    '''
    Create a comment if it is new, or update it if it exists.
    '''
    model_cme = None
    try:
        model_cme = GithubCommitComment.objects.get(comment_id=commentObj.id)
    except:
        model_cme = GithubCommitComment()
    model_cme.comment_id = commentObj.id
    model_cme.html_url = commentObj.html_url
    model_cme.body = commentObj.body
    model_cme.path = commentObj.path
    model_cme.position = commentObj.position
    model_cme.line = commentObj.line
    model_cme.commit_id = commentObj.commit_id
    model_cme.user = create_or_update_user(commentObj.user)
    model_cme.created_at = commentObj.created_at
    model_cme.updated_at = commentObj.updated_at
    model_cme.save()
    return model_cme

def create_or_update_pull_request(prequestObj, mProjectId):
    '''
    Create a pull request if it is new, or update it if it exists.
    '''
    model_prequest = None
    try:
        model_prequest = GithubPullRequest.objects.get(html_url=prequestObj.html_url)
    except:
        model_prequest = GithubPullRequest()
        model_prequest.m_project_id = mProjectId
    model_prequest.pull_request_id = prequestObj.id
    model_prequest.html_url = prequestObj.html_url
    model_prequest.issue_url = prequestObj.issue_url
    model_prequest.diff_url = prequestObj.diff_url
    model_prequest.number = prequestObj.number
    model_prequest.state = prequestObj.state
    model_prequest.title = prequestObj.title
    model_prequest.body = prequestObj.body
    model_prequest.created_at = prequestObj.created_at
    model_prequest.updated_at = prequestObj.updated_at
    model_prequest.closed_at = prequestObj.closed_at
    model_prequest.merged_at = prequestObj.merged_at
    model_prequest.merge_commit_sha = prequestObj.merge_commit_sha
    model_prequest.closed_at = prequestObj.closed_at

    # users
    if prequestObj.user is not None:
        model_prequest.user = create_or_update_user(prequestObj.user)
    if prequestObj.assignee is not None:
        model_prequest.assignee = create_or_update_user(prequestObj.assignee)
    model_prequest.save()
    
    
    assignee_ids = []
    for ass in prequestObj.assignees:
        assignee_ids.append(create_or_update_user(ass).id)
    model_prequest.assignees.set(list(GithubUser.objects.filter(id__in=assignee_ids)))

    reviewer_ids = []
    for rvr in prequestObj.get_review_requests()[0]:
        reviewer_ids.append(create_or_update_user(rvr).id)
    model_prequest.requested_reviewers.set(list(GithubUser.objects.filter(id__in=reviewer_ids)))

    model_prequest.save()

    # D Pull Request
    d_model_request = None
    try:
        d_model_request = DPullRequest.objects.get(url=prequestObj.html_url)
    except:
        d_model_request = DPullRequest()
        d_model_request.url = prequestObj.html_url
    d_model_request.project = DProjectToolInfo.objects.get(project_id=mProjectId)
    if prequestObj.user is not None:
        d_model_request.developer = DDeveloperToolMap.objects.get(developer_id = model_prequest.user.m_developer_id)
    d_model_request.title = prequestObj.title
    d_model_request.contents = prequestObj.body
    d_model_request.create_datetime = prequestObj.created_at
    d_model_request.merge_datetime = prequestObj.merged_at
    d_model_request.save()

    return model_prequest

def update_repository(confInfo):
    '''
    Manage a repository and its commits, comments and pull requests.
    '''
    g = Github(confInfo['token'])
    repo = g.get_repo(confInfo['target'])
    print(f"* -- Begin Github Repository {repo.full_name} -- *")
    try:
        model_repo = None
        try:
            model_repo = GithubRepository.objects.get(repo_id=repo.id)
        except:
            model_repo = GithubRepository()
        model_repo.repo_id = repo.id
        model_repo.name = repo.name
        model_repo.full_name = repo.full_name
        model_repo.owner = create_or_update_user(repo.owner)
        model_repo.description = repo.description
        model_repo.html_url = repo.html_url
        model_repo.default_branch = repo.default_branch
        model_repo.open_issues = repo.open_issues
        model_repo.open_issues_count = repo.open_issues_count
        model_repo.created_at = repo.created_at
        model_repo.updated_at = repo.updated_at
        model_repo.save()
        
        print("* -- Github Collaborators -- *")
        collaborators = repo.get_collaborators()
        collaborator_ids = []
        for cusr in collaborators:
            collaborator_ids.append(create_or_update_user(cusr).id)
        model_repo.collaborators.set(list(GithubUser.objects.filter(id__in=collaborator_ids)))

        print("* -- Github Assignees -- *")
        assignees = repo.get_assignees()
        assignee_ids = []
        for cusr in assignees:
            assignee_ids.append(create_or_update_user(cusr).id)
        model_repo.assignees.set(list(GithubUser.objects.filter(id__in=assignee_ids)))

        print("* -- Github Commits -- *")
        commits = repo.get_commits()
        commit_ids = []
        for cmt in commits:
            commit_ids.append(create_or_update_commit(cmt).id)
        model_repo.commits.set(list(GithubCommit.objects.filter(id__in=commit_ids)))

        print("* -- Github Comments -- *")
        commit_comments = repo.get_comments()
        comment_ids = []
        for cme in commit_comments:
            comment_ids.append(create_or_update_comment(cme).id)
        model_repo.commit_comments.set(list(GithubCommitComment.objects.filter(id__in=comment_ids)))

        print("* -- Github Pull Requests -- *")
        prequests = repo.get_pulls()
        prequest_ids = []
        for pr in prequests:
            prequest_ids.append(create_or_update_pull_request(pr, confInfo['project_id']).id)
        model_repo.pull_requests.set(list(GithubPullRequest.objects.filter(id__in=prequest_ids)))

        model_repo.save()

    except Exception as e:
        print("* -- ERROR OCCURED -- *")
        print(str(e))
    
    print(f"* -- End Github Repository {repo.full_name} -- *")

def get_github_pull_requests(start_time):
    '''
    Get pull requests and serialize them to return those as an API response.
    '''
    requests = []
    if start_time is None:
        requests = GithubPullRequest.objects.order_by('-id')
    else:
        requests = GithubPullRequest.objects.filter(Q(created_at__gte=start_time) | Q(updated_at__gte=start_time) | Q(closed_at__gte=start_time) | Q(merged_at__gte=start_time)).order_by('-id')
    
    requestSerializer = GithubPullRequestSerializer(requests, many=True)

    return requestSerializer.data

def get_github_prequest_reviewers(start_time):
    '''
    Get PR reviewers and serialize them to return those as an API response.
    '''
    requests = []
    if start_time is None:
        requests = GithubPullRequest.objects.annotate(num_reviewers=Count('requested_reviewers')).filter(num_reviewers__gt=0).values('id', 'requested_reviewers__m_developer_id')
    else:
        requests = GithubPullRequest.objects.annotate(num_reviewers=Count('requested_reviewers')).filter(num_reviewers__gt=0).filter(Q(created_at__gte=start_time) | Q(updated_at__gte=start_time) | Q(closed_at__gte=start_time) | Q(merged_at__gte=start_time)).values('id', 'requested_reviewers__m_developer_id')
    
    reviewerSerializer = GithubPrequestReviewerSerializer(requests, many=True)

    return reviewerSerializer.data