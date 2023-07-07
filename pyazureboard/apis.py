import requests
from base64 import b64encode

def crypt_token(username, password):
    """Returns a Basic Auth string."""
    username = username.encode('latin1')
    password = password.encode('latin1')
    authstr = 'Basic ' + b64encode(b':'.join((username, password))).strip().decode('ascii')
    return authstr

def arrange_response(res:requests.Response) -> dict | None:
    if res.status_code >= 200 and res.status_code < 300:
        data = res.json()
        return data
    else:
        return None

def get_project(domain_url:str, project_id:str, token:str) -> dict | None:
    encrypted_token = crypt_token('', token)
    project_url = f"{domain_url}/_apis/projects/{project_id}?api-version=6.0"
    res = requests.get(project_url, headers={'Authorization': encrypted_token})
    return arrange_response(res)

def get_workitems(domain_url:str, project_id:str, token:str) -> list | None:
    encrypted_token = crypt_token('', token)
    wiql_url = f"{domain_url}/{project_id}/_apis/wit/wiql?api-version=6.0"
    res = requests.post(
        wiql_url, 
        headers={'Authorization': encrypted_token},
        json={
            'query': 'Select [System.Id] From WorkItems'
        }
    )
    id_data = arrange_response(res)
    ids = []
    if id_data is None:
        return []
    else:
        ids=[str(wi['id']) for wi in id_data['workItems']]
        ids = ",".join(ids)
        workitem_url = f"{domain_url}/{project_id}/_apis/wit/workitems?ids={ids}&api-version=6.0"
        resp = requests.get(workitem_url, headers={'Authorization': encrypted_token})
        resp_data = arrange_response(resp)
        if resp_data is None:
            return []
        else:
            return resp_data['value']

def get_user_avatar(domain:str, descriptor:str, token:str) -> str | None:
    encrypted_token = crypt_token('', token)
    api_url = f"{domain.replace('https://dev.azure.com/', 'https://vssps.dev.azure.com/')}/_apis/graph/Subjects/{descriptor}/avatars?api-version=5.1-preview.1"
    res = requests.get(api_url, headers={'Authorization': encrypted_token})
    res_data = arrange_response(res)
    if res_data is None:
        return None
    else:
        return f"{res_data['value']}"

def get_iterations(domain_url:str, project_id:str, token:str) -> list | None:
    encrypted_token = crypt_token('', token)
    iteration_url = f"{domain_url}/{project_id}/_apis/work/teamsettings/iterations?timeframe=current&api-version=5.0"
    res = requests.get(iteration_url, headers={'Authorization': encrypted_token})
    res_data = arrange_response(res)
    if res_data is None:
        return None
    else:
        return res_data['value']

def get_wiki_identifiers(domain_url:str, project_id:str, token:str) -> list | None:
    encrypted_token = crypt_token('', token)
    api_url = f"{domain_url}/{project_id}/_apis/wiki/wikis?api-version=7.0"
    res = requests.get(api_url, headers={'Authorization': encrypted_token})
    res_data = arrange_response(res)
    if res_data is None:
        return None
    else:
        return res_data['value']

def get_wiki_pages(domain_url:str, project_id:str, wiki_identifier:str, path:str, token:str) -> list | None:
    encrypted_token = crypt_token('', token)
    api_url = f"{domain_url}/{project_id}/_apis/wiki/wikis/{wiki_identifier}/pages?recursionLevel=OneLevel&includeContent=True&api-version=7.0&path={path}"
    res = requests.get(api_url, headers={'Authorization': encrypted_token})
    res_data = arrange_response(res)
    if res_data is None:
        return None
    else:
        return res_data