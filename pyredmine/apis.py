import requests

# api management
def get_redmine_api(domain, url, api_access_key) -> dict:
    res = requests.get(f"{domain}/{url}", headers={"X-Redmine-API-Key": api_access_key})
    if res.status_code == 200:
        return {"success": True, "data": res.json()}
    else:
        return {"success": False}

def get_redmine_projects(domain, api_access_key) -> dict:
    return get_redmine_api(domain, 'projects.json', api_access_key)

def get_redmine_project(domain, api_access_key, project_id) -> dict:
    return get_redmine_api(domain, f'projects/{project_id}.json', api_access_key)

def get_redmine_users(domain, api_access_key) -> dict:
    return get_redmine_api(domain, 'users.json', api_access_key)

def get_redmine_trackers(domain, api_access_key) -> dict:
    return get_redmine_api(domain, 'trackers.json', api_access_key)

def get_redmine_statuses(domain, api_access_key) -> dict:
    return get_redmine_api(domain, 'issue_statuses.json', api_access_key)

def get_redmine_issues(domain, api_access_key) -> dict:
    return get_redmine_api(domain, 'issues.json', api_access_key)

def get_redmine_project_files(domain, project_id, api_access_key) -> dict:
    return get_redmine_api(domain, f'projects/{project_id}/files.json', api_access_key)

def get_redmine_wikis(domain, project_identifier, api_access_key) -> dict:
    return get_redmine_api(domain, f'projects/{project_identifier}/wiki/index.json', api_access_key)

def get_redmine_wiki(domain, project_identifier, title, api_access_key) -> dict:
    return get_redmine_api(domain, f'projects/{project_identifier}/wiki/{title}.json', api_access_key)

def get_redmine_versions(domain, project_identifier, api_access_key) -> dict:
    return get_redmine_api(domain, f'projects/{project_identifier}/versions.json', api_access_key)

def get_redmine_version(domain, version_identifier, api_access_key) -> dict:
    return get_redmine_api(domain, f'versions/{version_identifier}.json', api_access_key)