import requests

def is_status_ok(status_code):
    if status_code >= 200 and status_code < 300:
        return True
    else:
        return False

def get_trello_api(url, appKey, appToken):
    res = requests.get(f'https://api.trello.com{url}?key={appKey}&token={appToken}')
    if is_status_ok(res.status_code):
        return {
            'success': True,
            'data': res.json()
        }
    else:
        print('API ERROR', res.status_code)
        print(res.text)
        return {'success': False}

def get_all_boards(appKey, appToken):
    return get_trello_api('/1/members/me/boards', appKey, appToken)

def get_board_data(appKey, appToken, boardId):
    return get_trello_api(f'/1/boards/{boardId}', appKey, appToken)

def get_all_board_lists(appKey, appToken, boardId):
    return get_trello_api(f'/1/boards/{boardId}/lists', appKey, appToken)

def get_all_board_cards(appKey, appToken, boardId):
    return get_trello_api(f'/1/boards/{boardId}/cards', appKey, appToken)

def get_all_board_actions(appKey, appToken, boardId):
    return get_trello_api(f'/1/boards/{boardId}/actions', appKey, appToken)

def get_user_info(appKey, appToken, userId):
    return get_trello_api(f'/1/members/{userId}', appKey, appToken)
