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
from .apis import get_all_board_actions, get_all_board_cards, get_all_board_lists, get_board_data, get_user_info
from .models import TrelloBoard, TrelloUser, TrelloList, TrelloCard, TrelloAction
from .serializers import TrelloCardSerializer
from dbanalysis.models import DDeveloperToolMap, TOOL_INDICES
from dbanalysis.s3utils import create_boto3_session, create_object_key, upload_s3_from_url

def create_or_update_user(appKey, appToken, userId):
    '''
    Create a user if it is new, or update it if it exists.
    '''

    if userId is None:
        return None

    try:
        user_api_data = get_user_info(appKey, appToken, userId)
        if user_api_data['success']:
            model_user = None
            try:
                model_user = TrelloUser.objects.get(userId=userId)
            except:
                model_user = TrelloUser()
                model_user.userId = userId
            
            model_user.username = user_api_data['data'].get('username')
            model_user.fullName = user_api_data['data'].get('fullName')
            model_user.initials = user_api_data['data'].get('initials')
            model_user.avatarHash = user_api_data['data'].get('avatarHash')
            model_user.avatarUrl = user_api_data['data'].get('avatarUrl')
            if model_user.avatarUrl:
                model_user.avatarUrl = model_user.avatarUrl + "/50.png"
            model_user.nonPublicAvailable = user_api_data['data'].get('nonPublicAvailable')
            model_user.memberType = user_api_data['data'].get('memberType')
            model_user.userUrl = user_api_data['data'].get('url')
            model_user.email = user_api_data['data'].get('email')

            # developer map
            m_developer_data = DDeveloperToolMap.objects.filter(Q(tool_id=TOOL_INDICES['trello']) & Q(account_name = user_api_data['data'].get('username')))
            if m_developer_data.count() > 0:
                m_developer = m_developer_data.first()
                if model_user.m_developer_id is None:
                    model_user.m_developer_id = m_developer.developer_id
                if (m_developer.s3_bucket_key is None) and (model_user.avatarUrl is not None):
                    my_session = create_boto3_session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_REGION_NAME)
                    object_key = upload_s3_from_url(my_session, settings.AWS_STORAGE_BUCKET_NAME, model_user.avatarUrl, create_object_key('png'))
                    m_developer.s3_bucket_key = object_key
                    m_developer.save()

            model_user.save()

            return model_user

        else:
            return None

    except Exception as err:
        print("trello user error")
        print(str(err))

def create_or_update_board(boardInfo: dict, conf: dict):
    '''
    Create a board if it is new, or update it if it exists.
    '''

    try:
        model_board = None
        try:
            model_board = TrelloBoard.objects.get(boardId=boardInfo['id'])
        except:
            model_board = TrelloBoard()
            model_board.boardId = boardInfo['id']
        model_board.m_project_id = conf['project_id']
        model_board.name = boardInfo.get('name')
        model_board.desc = boardInfo.get('desc')
        model_board.closed = boardInfo.get('closed')
        model_board.idOrganization = boardInfo.get('idOrganization')
        model_board.boardUrl = boardInfo.get('url')
        model_board.shortUrl = boardInfo.get('shortUrl')
        model_board.dateLastActivity = boardInfo.get('dateLastActivity')
        model_board.dateLastView = boardInfo.get('dateLastView')
        model_board.ixUpdate = boardInfo.get('ixUpdate')

        model_board.memberCreator = create_or_update_user(conf['target'], conf['token'], boardInfo.get('idMemberCreator'))

        model_board.save()
        
        return model_board

    except Exception as err:
        print("trello board error")
        print(str(err))

def create_or_update_list(listInfo: dict, boardObj: TrelloBoard):
    '''
    Create a list if it is new, or update it if it exists.
    '''

    try:
        model_list = None
        try:
            model_list = TrelloList.objects.get(listId = listInfo['id'])
        except:
            model_list = TrelloList()
            model_list.listId = listInfo['id']
        
        model_list.name = listInfo.get('name')
        model_list.closed = listInfo.get('closed')
        model_list.pos = listInfo.get('pos')
        model_list.board = boardObj
        
        model_list.save()

        return model_list
    
    except Exception as err:
        print("trello list error")
        print(str(err))

def create_or_update_card(cardInfo: dict, boardObj: TrelloBoard, conf: dict):
    '''
    Create a card if it is new, or update it if it exists.
    '''

    try:
        model_card = None
        try:
            model_card = TrelloCard.objects.get(cardId=cardInfo['id'])
        except:
            model_card = TrelloCard()
            model_card.cardId = cardInfo['id']

        model_card.name = cardInfo.get('name')
        model_card.desc = cardInfo.get('desc')
        model_card.closed = cardInfo.get('closed')
        model_card.dueComplete = cardInfo.get('dueComplete')
        model_card.email = cardInfo.get('email')
        model_card.isTemplate = cardInfo.get('isTemplate')
        model_card.pos = cardInfo.get('pos')
        model_card.shortLink = cardInfo.get('shortLink')
        model_card.shortUrl = cardInfo.get('shortUrl')
        model_card.cardUrl = cardInfo.get('url')
        model_card.dateLastActivity = cardInfo.get('dateLastActivity')
        model_card.start = cardInfo.get('start')
        model_card.due = cardInfo.get('due')
        model_card.board = boardObj
        if cardInfo.get('idList'):
            model_card.list = TrelloList.objects.get(listId = cardInfo.get('idList'))
        
        model_card.save()

        memIds = []
        for memId in cardInfo['idMembers']:
            memIds.append(create_or_update_user(conf['target'], conf['token'], memId).id)
        model_card.members.set(list(TrelloUser.objects.filter(id__in=memIds)))

        memIds = []
        for memId in cardInfo['idMembersVoted']:
            memIds.append(create_or_update_user(conf['target'], conf['token'], memId).id)
        model_card.votedMembers.set(list(TrelloUser.objects.filter(id__in=memIds)))

        model_card.save()

    except Exception as err:
        print("trello card error")
        print(str(err)) 

def create_or_update_action(actionInfo: dict, conf: dict):
    '''
    Create an action if it is new, or update it if it exists.
    '''

    try:
        model_action = None
        try:
            model_action = TrelloAction.objects.get(actionId = actionInfo['id'])
        except:
            model_action = TrelloAction()
            model_action.actionId = actionInfo['id']

        model_action.data = actionInfo.get('data')
        model_action.type = actionInfo.get('type')
        model_action.date = actionInfo.get('date')

        if actionInfo.get('appCreator') is not None:
            model_action.appCreator = create_or_update_user(conf['target'], conf['token'], actionInfo['appCreator']['id'])

        if actionInfo.get('member') is not None:
            model_action.member = create_or_update_user(conf['target'], conf['token'], actionInfo['member']['id'])

        if actionInfo.get('idMemberCreator') is not None:
            model_action.memberCreator = create_or_update_user(conf['target'], conf['token'], actionInfo['idMemberCreator'])

        model_action.save()

        return model_action

    except Exception as err:
        print("trello action error")
        print(str(err))

def update_board(conf):
    '''
    Manage a selected board and its board lists, cards and actions.
    '''

    try:
        api_data = get_board_data(conf['target'], conf['token'], conf['payload'])
        if api_data['success']:
            bd = api_data['data']
            print(f"Board {bd['id']} begin")

            bd_obj = create_or_update_board(bd, conf)
            # lists
            list_api_data = get_all_board_lists(conf['target'], conf['token'], bd_obj.boardId)
            if list_api_data['success']:
                for lst in list_api_data['data']:
                    create_or_update_list(lst, bd_obj)

            # cards
            card_api_data = get_all_board_cards(conf['target'], conf['token'], bd_obj.boardId)
            if card_api_data['success']:
                for crd in card_api_data['data']:
                    create_or_update_card(crd, bd_obj, conf)

            # actions
            action_api_data = get_all_board_actions(conf['target'], conf['token'], bd_obj.boardId)
            if action_api_data['success']:
                for actn in action_api_data['data']:
                    create_or_update_action(actn, conf)

            print(f"Board {bd['id']} end")
        
    except Exception as err:
        print("ERROR OCCURED")
        print(str(err))

def get_trello_cards(start_time):
    '''
    Get board cards as tickets and serialize them to return those as an API response.
    '''

    cards = []

    if start_time is None:
        cards = TrelloCard.objects.order_by('-id')
    else:
        cards = TrelloCard.objects.filter(Q(reg_date__gte=start_time) | (Q(dateLastActivity__isnull=False) & Q(dateLastActivity__gte=start_time))).order_by('-id')

    serializer = TrelloCardSerializer(cards, many=True)

    return serializer.data

