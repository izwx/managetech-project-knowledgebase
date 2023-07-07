import requests
import base64

def execute_api(url_part: str, domain_name: str, api_key: str) -> dict | None:
    api_url = f"{domain_name}/api/v2/{url_part}?apiKey={api_key}"
    res = requests.get(api_url)
    if res.status_code >= 200 and res.status_code < 300:
        data = res.json()
        return data
    else:
        return None

def get_projects(domain_name: str, api_key: str) -> list | None:
    return execute_api('projects', domain_name, api_key)

def get_project_info(domain_name: str, api_key: str, project_id: str | int) -> dict | None:
    return execute_api(f'projects/{project_id}', domain_name, api_key)

def get_issues(domain_name: str, api_key: str, project_id: str | int) -> list | None:
    return execute_api(f'issues', domain_name, f"{api_key}&projectId[]={project_id}") 

def get_versions(domain_name: str, api_key: str, project_id: str | int) -> list | None:
    return execute_api(f'projects/{project_id}/versions', domain_name, api_key) 

def get_users(domain_name: str, api_key: str) -> list | None:
    return execute_api('users', domain_name, api_key)  

def get_wikis(domain_name: str, api_key: str, project_id: str | int) -> list | None:
    return execute_api('wikis', domain_name, f"{api_key}&projectIdOrKey={project_id}")

def get_user_icon(domain_name: str, api_key: str, user_id: int) -> str | None:
    api_url = f"{domain_name}/api/v2/users/{user_id}/icon?apiKey={api_key}"
    res = requests.get(api_url)
    # return data
    b64_string = None
    if res.status_code >= 200 and res.status_code < 300:
        try:
            b64_string = base64.b64encode(res.content).decode()
            b64_string = 'data:' + res.headers['Content-Type'] + ';base64,' + b64_string
        except Exception as err:
            print(str(err))
            b64_string = None
    return b64_string