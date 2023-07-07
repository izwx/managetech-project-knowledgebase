import requests

def is_status_ok(status_code):
    if status_code == 204:
        return False
    if status_code >= 200 and status_code < 300:
        return True
    else:
        return False

def get_chatwork_api(url, api_token):
    res = requests.get(
        f"https://api.chatwork.com/v2{url}",
        headers={
            'X-ChatWorkToken': api_token
        }
    )

    if is_status_ok(res.status_code):
        return {
            'success': True,
            'data': res.json()
        }
    else:
        print('API ERROR', res.status_code, url)
        print(res.text)
        return {'success': False, 'status_code': res.status_code}


def get_all_rooms(api_token):
    return get_chatwork_api('/rooms', api_token)

def get_room_info(room_id, api_token):
    return get_chatwork_api(f'/rooms/{room_id}', api_token)

def get_all_room_members(room_id, api_token):
    return get_chatwork_api(f'/rooms/{room_id}/members', api_token)

def get_all_room_messages(room_id, api_token):
    return get_chatwork_api(f'/rooms/{room_id}/messages?force=1', api_token)

def get_all_room_tasks(room_id, api_token):
    return get_chatwork_api(f'/rooms/{room_id}/tasks', api_token)

def get_all_room_files(room_id, api_token):
    return get_chatwork_api(f'/rooms/{room_id}/files', api_token)