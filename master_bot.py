import cfg
import secrets
import string
from datetime import datetime
from vk_utils import *
from enum import Enum
from audio_box import AudioBOX


class Modes(Enum):
    PLAY_MORSE = 0
    DO_CMD = 1


class MasterBot:
    MAX_CMD_LEN = 5

    def __init__(self, ):
        self.states = [True, False]

    def do(self):
        to_mark_as_read_ids = []
        if self.states[Modes.PLAY_MORSE.value]:
            params = {'count': 200, 'filter': 'unread'}
            unread_chats = cfg.vk.method('messages.getConversations', params)['items']
            for item in unread_chats:
                unread_count = item['conversation']['unread_count']
                chat_id = item['conversation']['peer']['id']
                params = {'count': unread_count, 'user_id': chat_id}
                chat_messages = cfg.vk.method('messages.getHistory', params)['items']
                chat_messages.reverse()
                for u_msg in chat_messages:
                    name = name_from_id(u_msg['from_id'])
                    cur_time = datetime.fromtimestamp(u_msg['date'])
                    f_time = str(datetime.strftime(cur_time, "%H:%M")) + ' -> '
                    print(f_time, name, ': ', u_msg['text'], sep='')
                    text = u_msg['text']
                    AudioBOX.play_morse(text, 0.15)
                to_mark_as_read_ids.append(chat_id)

        if self.states[Modes.DO_CMD.value]:
            unread_messages = get_unread_messages()
            for u_msg in unread_messages:
                text = u_msg['text']
                peer_id = u_msg['peer_id']
                chunks = text[:self.MAX_CMD_LEN].split()
                if not chunks:
                    continue
                chunk = chunks[0]
                if chunk == '/pi':
                    post_msg({'peer_id': peer_id},
                             '3,1415926535 8979323846 2643383279 5028841971 6939937510 5820974944 5923078164 0628620899 8628034825 3421170679 8214808651 3282306647 0938446095 5058223172 5359408128 4811174502 8410270193 8521105559 6446229489 5493038196 4428810975 6659334461 2847564823 3786783165 2712019091 4564856692 3460348610 4543266482 1339360726 0249141273 7245870066 0631558817 4881520920 9628292540 9171536436 7892590360 0113305305 4882046652 1384146951 9415116094 3305727036 5759591953 0921861173 8193261179 3105118548 0744623799 6274956735 1885752724 8912279381 8301194912 9833673362 4406566430 8602139494 6395224737 1907021798 6094370277 0539217176 2931767523 8467481846 7669405132 0005681271 4526356082 7785771342 7577896091 7363717872 1468440901 2249534301 4654958537 1050792279 6892589235 4201995611 2129021960 8640344181 5981362977 4771309960 5187072113 4999999837 2978049951 0597317328 1609631859 5024459455 3469083026 4252230825 3344685035 2619311881 7101000313 7838752886 5875332083 8142061717 7669147303 5982534904 2875546873 1159562863 8823537875 9375195778 1857780532 1712268066 1300192787 6611195909 2164201989')
                if chunk == '/rnd':
                    msg = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(3500))
                    post_msg({'peer_id': peer_id}, msg)

        for chat_id in to_mark_as_read_ids:
            cfg.vk.method('messages.markAsRead', {'peer_id': chat_id})
