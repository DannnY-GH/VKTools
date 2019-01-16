import copy
from vk_utils import *

trackAmt = 200


class Target:
    def __init__(self, id):
        self.id = id
        self.prev_hist = []


class WatchdogBot:
    def __init__(self):
        self.targets = []
        self.log_file = 'log.txt'
        self.send_back = False
        open(self.log_file, 'w').close()

    def add_target(self, id):
        self.targets.append(Target(id))

    def log(self, msg):
        file = open(self.log_file, 'a')
        file.write(msg + "\n")
        file.close()
        print(msg)

    def update_target(self, target):
        cur_response = get_messages(target.id, trackAmt)
        cur_response.reverse()
        if cur_response:
            if cur_response[0] in target.prev_hist:
                prev_pos = target.prev_hist.index(cur_response[0])
                cur_pos = 0
                while prev_pos < len(target.prev_hist):
                    prev = target.prev_hist[prev_pos]
                    msg_params = {'peer_id': prev['peer_id']}
                    if cur_pos >= len(cur_response):
                        sender_name = name_from_id(prev['from_id'])  # saving time
                        msg = sender_name + ' deleted (' + prev['text'] + ')'
                        if self.send_back:
                            post_msg(msg_params, msg)
                        self.log(msg)
                    else:
                        cur = cur_response[cur_pos]
                        if cur['id'] != prev['id']:
                            sender_name = name_from_id(prev['from_id'])  # saving time
                            msg = sender_name + ' deleted (' + prev['text'] + ')'
                            if self.send_back:
                                post_msg(msg_params, msg)
                            self.log(msg)
                            cur_pos -= 1
                        elif cur['text'] != prev['text']:
                            sender_name = name_from_id(prev['from_id'])  # saving time
                            msg = sender_name + ' changed (' + prev['text'] + ')' + ' to (' + cur['text'] + ')'
                            if self.send_back:
                                post_msg(msg_params, msg)
                            self.log(msg)
                    cur_pos += 1
                    prev_pos += 1
            target.prev_hist = copy.deepcopy(cur_response)

    def update(self):
        for target in self.targets:
            self.update_target(target)
