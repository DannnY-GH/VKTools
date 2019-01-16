import random
import cfg
import time

MSG_LIMIT = 200


def get_unread_messages():
    unread_messages = []
    params = {'count': 200, 'filter': 'unread'}
    unread_chats = cfg.vk.method('messages.getConversations', params)['items']
    for item in unread_chats:
        unread_count = item['conversation']['unread_count']
        chat_id = item['conversation']['peer']['id']
        params = {'count': unread_count, 'user_id': chat_id}
        unread_messages.extend(cfg.vk.method('messages.getHistory', params)['items'])
    return unread_messages


def post_msg(params, s):
    params['message'] = s
    params['random_id'] = random.randint(0, 2 ** 32 - 1)
    cfg.vk.method('messages.send', params)


def id_from_screen_name(screen_name):
    cur_response = cfg.vk.method('users.get', {'user_ids': {screen_name}})
    return cur_response[0]['id']


def name_from_id(id):
    cur_response = cfg.vk.method('users.get', {'user_ids': {id}})
    return cur_response[0]['first_name'] + ' ' + cur_response[0]['last_name']


def get_user_friends(id):
    params = {'user_id': id, 'count': 5000,
              'order': 'name', 'fields': {'name'}}
    return cfg.vk.method('friends.get', params)


def convert_to_ids(screen_list):
    for ind, e in enumerate(screen_list):
        screen_list[ind] = id_from_screen_name(e)


def get_user_friend_ids(user_id):
    friends = get_user_friends(user_id)['items']
    for i in range(len(friends)):
        friends[i] = friends[i]['id']
    return friends


def get_messages(id, left):
    msg = []
    params = {'count': MSG_LIMIT, 'user_id': id, 'start_message_id': -1}
    while left > 0:
        params['count'] = min(MSG_LIMIT, left)
        items = cfg.vk.method('messages.getHistory', params)['items']
        if not items:
            break
        msg.extend(items)
        params['start_message_id'] = items[-1]['id']
        params['offset'] = 1
        left -= MSG_LIMIT
        time.sleep(0.1)
    return msg
