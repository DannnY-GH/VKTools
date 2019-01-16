import time
import cfg
from watchdog_bot import WatchdogBot
from master_bot import MasterBot

cfg.init()

'''
watchdog_bot = WatchdogBot()
watchdog_bot.add_target(CHAT_ID)
while True:
    watchdog_bot.update()
    time.sleep(0.3)
'''

master_bot = MasterBot()
while True:
    master_bot.do()
    time.sleep(0.3)
