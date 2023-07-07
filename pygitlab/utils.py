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

from django.db.models import Q, Count
from django.conf import settings
import gitlab
from datetime import datetime
import pytz
from .models import (
    GitlabGroup, GitlabProject, GitlabUser,
    GitlabBranch, GitlabCommit, GitlabMergeRequest, 
    GitlabWiki,
)
from dbanalysis.models import DProjectToolInfo, DDeveloperToolMap, TOOL_INDICES, DPullRequest, DDocument
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url
from .serializers import GitlabWikiSerializer, GitlabMergeRequestSerializer, GitlabPrequestReviewerSerializer

def create_or_update_user(userData):
    '''
    Create a user if it is new, or update it if it exists.
    '''

    print(f"* -- -- gitlab user {userData['id']} -- -- *")
    user_model = None
    try:
        user_model = GitlabUser.objects.get(user_id=userData['id'])
    except:
        user_model = GitlabUser()
        user_model.user_id = userData['id']

    user_model.username = userData['username']
    user_model.web_url = userData['web_url']
    user_model.name = userData['name']
    user_model.state = userData['state']
    user_model.avatar_url = userData['avatar_url']
    user_model.created_at = userData['created_at']

    # developer map
    
    m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['gitlab']) & Q(account_name = userData['web_url']))
    if m_developer_data.count() > 0:
        m_developer = m_developer_data.first()
        if user_model.m_developer_id is None:
            user_model.m_developer_id = m_developer.developer_id
        if m_developer.s3_bucket_key is None:
            my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
            object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, user_model.avatar_url, create_object_key('png'))
            m_developer.s3_bucket_key = object_key
            m_developer.save()


    user_model.save()

    return user_model

def create_or_update_branch(branchData):
    '''
    Create a branch if it is new, or update it if it exists.
    '''

    print(f"* -- -- gitlab branch {branchData['web_url']} -- -- *")
    brnch_model = None
    try:
        brnch_model = GitlabBranch.objects.get(web_url=branchData['web_url'])
    except:
        brnch_model = GitlabBranch()
        brnch_model.web_url = branchData['web_url']
    
    brnch_model.name = branchData['name']
    brnch_model.merged = branchData['merged']
    brnch_model.protected = branchData['protected']
    brnch_model.default = branchData['default']
    
    brnch_model.save()

    return brnch_model

def create_or_update_commit(commitData):
    '''
    Create a commit if it is new, or update it if it exists.
    '''

    print(f"* -- -- gitlab commit {commitData['web_url']} -- -- *")
    commit_model = None
    try:
        commit_model = GitlabCommit.objects.get(web_url = commitData['web_url'])
    except:
        commit_model = GitlabCommit()
        commit_model.commit_id = commitData['id']
        commit_model.short_id = commitData['short_id']

    commit_model.title = commitData['title']
    commit_model.message = commitData['message']
    commit_model.web_url = commitData['web_url']
    commit_model.created_at = commitData['created_at']

    # author
    commit_model.author_name = commitData['author_name']
    commit_model.author_email = commitData['author_email']
    commit_model.authored_date = commitData['authored_date']
    # committer
    commit_model.committer_name = commitData['committer_name']
    commit_model.committer_email = commitData['committer_email']
    commit_model.committed_date = commitData['committed_date']

    commit_model.save()

    return commit_model

def create_or_update_merge_request(mergeRequestData, mProjectId):
    '''
    Create a merge request as a pull request if it is new, or update it if it exists.
    '''

    print(f"* -- -- gitlab merge_request {mergeRequestData['web_url']} -- -- *")
    mrequest_model = None
    try:
        mrequest_model = GitlabMergeRequest.objects.get(web_url = mergeRequestData['web_url'])
    except:
        mrequest_model = GitlabMergeRequest()
        mrequest_model.request_id = mergeRequestData['id']
        mrequest_model.request_iid = mergeRequestData['iid']
        mrequest_model.web_url = mergeRequestData['web_url']
        mrequest_model.m_project_id = mProjectId

    mrequest_model.title = mergeRequestData['title']
    mrequest_model.description = mergeRequestData['description']
    mrequest_model.state = mergeRequestData['state']
    if mergeRequestData['merge_user'] is not None:
        mrequest_model.merge_user = GitlabUser.objects.get(web_url = mergeRequestData['merge_user']['web_url'])
    mrequest_model.merged_at = mergeRequestData['merged_at']
    if mergeRequestData['closed_by'] is not None:
        mrequest_model.closed_by = GitlabUser.objects.get(web_url = mergeRequestData['closed_by']['web_url'])
    mrequest_model.closed_at = mergeRequestData['closed_at']
    mrequest_model.created_at = mergeRequestData['created_at']
    mrequest_model.updated_at = mergeRequestData['updated_at']
    mrequest_model.target_branch = mergeRequestData['target_branch']
    mrequest_model.source_branch = mergeRequestData['source_branch']
    mrequest_model.upvotes = mergeRequestData['upvotes']
    mrequest_model.downvotes = mergeRequestData['downvotes']
    if mergeRequestData['author'] is not None:
        mrequest_model.author = GitlabUser.objects.get(web_url = mergeRequestData['author']['web_url'])
    if mergeRequestData['assignee'] is not None:
        mrequest_model.assignee = GitlabUser.objects.get(web_url = mergeRequestData['assignee']['web_url'])
    mrequest_model.save()

    assignee_urls = []
    for usr in mergeRequestData['assignees']:
        assignee_urls.append(usr['web_url'])
    mrequest_model.assignees.set(list(GitlabUser.objects.filter(web_url__in=assignee_urls)))

    reviewer_urls = []
    for usr in mergeRequestData['reviewers']:
        reviewer_urls.append(usr['web_url'])
    mrequest_model.reviewers.set(list(GitlabUser.objects.filter(web_url__in=reviewer_urls)))

    if mergeRequestData['draft'] is not None:
        mrequest_model.draft = mergeRequestData['draft']
    if mergeRequestData['work_in_progress'] is not None:
        mrequest_model.work_in_progress = mergeRequestData['work_in_progress']

    mrequest_model.save()

    # D Pull Request
    d_request_model = None
    try:
        d_request_model = DPullRequest.objects.get(url = mergeRequestData['web_url'])
    except:
        d_request_model = DPullRequest()
        d_request_model.url = mergeRequestData['web_url']
    d_request_model.project = DProjectToolInfo.objects.get(project_id=mProjectId)
    d_request_model.title = mergeRequestData['title']
    d_request_model.contents = mergeRequestData['description']
    d_request_model.create_datetime = mergeRequestData['created_at']
    d_request_model.merge_datetime = mergeRequestData['closed_at']

    if mergeRequestData['author'] is not None:
        d_request_model.developer = DDeveloperToolMap.objects.get(developer_id = mrequest_model.author.m_developer_id)

    d_request_model.save()

    return mrequest_model

def create_or_update_wiki(wikiData, projectGroupObj, group_or_project, m_project_id):
    '''
    Create a wiki document if it is new, or update it if it exists.
    '''

    print(f"* -- -- gitlab wiki {wikiData['project_id']} / {wikiData['slug']} -- -- *")
    wiki_model = None
    try:
        wiki_model = GitlabWiki.objects.get(wiki_id = f"{wikiData['project_id']}.{wikiData['slug']}")
    except:
        wiki_model = GitlabWiki()
        wiki_model.wiki_id = f"{wikiData['project_id']}.{wikiData['slug']}"
        wiki_model.m_project_id = m_project_id
    
    wiki_model.format = wikiData['format']
    wiki_model.slug = wikiData['slug']
    wiki_model.title = wikiData['title']
    wiki_model.encoding = wikiData.get('encoding')
    wiki_model.group_or_project = group_or_project

    wiki_page = projectGroupObj.wikis.get(wikiData['slug']) 
    wiki_model.content = wiki_page.content
    wiki_model.save()

    d_wiki_model = None
    try:
        d_wiki_model = DDocument.objects.get(Q(project__project_id=m_project_id) & Q(title=wikiData['title']))
        if d_wiki_model.contents != wiki_page.content:
            d_wiki_model.contents = wiki_page.content
            d_wiki_model.updated_at = datetime.now(tz=pytz.UTC)
    except:
        d_wiki_model = DDocument()
        d_wiki_model.project = DProjectToolInfo.objects.get(project_id = m_project_id)
        d_wiki_model.title = wikiData['title']
        d_wiki_model.contents = wiki_page.content
    
    d_wiki_model.save()

    return wiki_model

def create_or_update_group(groupData, memberData=[], wikiData=[]):
    '''
    Create a group if it is new, or update it if it exists.
    '''

    group_model = None
    try:
        group_model = GitlabGroup.objects.get(group_id=groupData['id'])
    except:
        group_model = GitlabGroup()
        group_model.group_id = groupData['id']
        
    group_model.web_url = groupData['web_url']
    group_model.name = groupData['name']
    group_model.path = groupData['path']
    group_model.description = groupData['description']
    group_model.visibility = groupData['visibility']
    group_model.avatar_url = groupData['avatar_url']
    group_model.full_name = groupData['full_name']
    group_model.full_path = groupData['full_path']
    group_model.created_at = groupData['created_at']
    group_model.save()

    # members
    member_ids = []
    for mbrObj in memberData:
        mbr = create_or_update_user(mbrObj)
        member_ids.append(mbr.id)
    group_model.members.set(GitlabUser.objects.filter(id__in=member_ids))
    
    # wiki
    wiki_ids = []
    for wkObj in wikiData:
        wk = create_or_update_wiki(wkObj, True)
        wiki_ids.append(wk.id)
    group_model.wikis.set(GitlabWiki.objects.filter(id__in=wiki_ids))

    group_model.save()

    return group_model

def create_or_update_project(
        projectData, creatorData, memberData=[], branchData=[], commitData=[], mrequestData=[], wikiData=[], projectObj=None,
        m_project_id=None
    ):
    '''
    Create a project if it is new, or update it if it exists.
    And manage its members, branches, commits, merge requests and wiki documents.
    '''

    print(f"* -- -- gitlab project {projectData['id']} -- -- *")
    project_model = None
    try:
        project_model = GitlabProject.objects.get(project_id=projectData['id'])
    except:
        project_model = GitlabProject()
        project_model.project_id = projectData['id']
    
    project_model.web_url = projectData['web_url']
    project_model.name = projectData['name']
    project_model.name_with_namespace = projectData['name_with_namespace']
    project_model.path = projectData['path']
    project_model.path_with_namespace = projectData['path_with_namespace']
    project_model.default_branch = projectData['default_branch']
    project_model.readme_url = projectData['readme_url']
    project_model.avatar_url = projectData['avatar_url']
    project_model.empty_repo = projectData['empty_repo']
    project_model.archived = projectData['archived']
    project_model.visibility = projectData['visibility']
    project_model.created_at = projectData['created_at']
    project_model.last_activity_at = projectData['last_activity_at']
    project_model.creator = create_or_update_user(creatorData)
    project_model.save()
    
    # members
    member_ids = []
    for mbrObj in memberData:
        mbr = create_or_update_user(mbrObj)
        member_ids.append(mbr.id)
    project_model.members.set(GitlabUser.objects.filter(id__in=member_ids))
    
    # branches 
    branch_ids = []
    for brnObj in branchData:
        brn = create_or_update_branch(brnObj)
        branch_ids.append(brn.id)
    project_model.branches.set(GitlabBranch.objects.filter(id__in=branch_ids))

    # commits
    commit_ids = []
    for cmtObj in commitData:
        cmt = create_or_update_commit(cmtObj)
        commit_ids.append(cmt.id)
    project_model.commits.set(GitlabCommit.objects.filter(id__in=commit_ids))

    # merge requests
    mrequest_ids = []
    for mrObj in mrequestData:
        mr = create_or_update_merge_request(mrObj, m_project_id)
        mrequest_ids.append(mr.id)
    project_model.merge_requests.set(GitlabMergeRequest.objects.filter(id__in=mrequest_ids))

    # wikis
    wiki_ids = []
    for wkObj in wikiData:
        wk = create_or_update_wiki(wkObj, projectObj, False, m_project_id)
        wiki_ids.append(wk.id)
    project_model.wikis.set(GitlabWiki.objects.filter(id__in=wiki_ids))

    project_model.save()

    return project_model

def update_group_and_project(confInfo):
    '''
    Manage a selected project and its members, branches, commits, merge requests and wiki documents.
    '''

    try:
        gl = gitlab.Gitlab(url=confInfo['target'], private_token=confInfo['token'])

        # project
        if confInfo['payload']:
            print(f"* -- gitlab Project {confInfo['payload']} -- *")
            prj = gl.projects.get(confInfo['payload'])
            creatorData = gl.users.get(prj.attributes['creator_id']).attributes
            print("* -- gitlab members -- *")
            members = [ mbr.attributes for mbr in prj.members.list() ]
            print("* -- gitlab branches -- *")
            branches = [ brc.attributes for brc in prj.branches.list() ]
            print("* -- gitlab commits -- *")
            commits = [ cmt.attributes for cmt in prj.commits.list() ]
            print("* -- gitlab merge requests -- *")
            mrequests = [ mr.attributes for mr in prj.mergerequests.list() ]
            print("* -- gitlab project wikis -- *")
            wikis = [ wk.attributes for wk in prj.wikis.list() ]
            create_or_update_project(prj.attributes, creatorData, members, branches, commits, mrequests, wikis, prj, confInfo['project_id'])

    except Exception as err:
        print("* -- ERROR OCCURED -- *")
        print(str(err))

def get_gitlab_documents(start_time):
    '''
    Get wiki documents and serialize them to return those as an API response.
    '''

    documents = []

    if start_time is None:
        documents = GitlabWiki.objects.order_by('-id')
    else:
        documents = GitlabWiki.objects.filter(reg_date__gte=start_time).order_by('-id')
    documentSerializer = GitlabWikiSerializer(documents, many=True)

    return documentSerializer.data


def get_gitlab_pull_requests(start_time):
    '''
    Get merge requests as PRs and serialize them to return those as an API response.
    '''

    requests = []
    if start_time is None:
        requests = GitlabMergeRequest.objects.order_by('-id')
    else:
        requests = GitlabMergeRequest.objects.filter(Q(created_at__gte=start_time) | Q(updated_at__gte=start_time) | Q(closed_at__gte=start_time) | Q(merged_at__gte=start_time)).order_by('-id')
    
    requestSerializer = GitlabMergeRequestSerializer(requests, many=True)

    return requestSerializer.data

def get_gitlab_prequest_reviewers(start_time):
    '''
    Get PR reviewers and serialize them to return those as an API response.
    '''

    requests = []
    if start_time is None:
        requests = GitlabMergeRequest.objects.annotate(num_reviewers=Count('reviewers')).filter(num_reviewers__gt=0).values('id', 'reviewers__m_developer_id')
    else:
        requests = GitlabMergeRequest.objects.annotate(num_reviewers=Count('reviewers')).filter(num_reviewers__gt=0).filter(Q(created_at__gte=start_time) | Q(updated_at__gte=start_time) | Q(closed_at__gte=start_time) | Q(merged_at__gte=start_time)).values('id', 'reviewers__m_developer_id')
    
    requestSerializer = GitlabPrequestReviewerSerializer(requests, many=True)

    return requestSerializer.data