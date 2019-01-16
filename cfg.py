import vk_api
from audio_box import AudioBOX


def init():
    global vk
    vk = vk_api.VkApi(login='YOUR LOGIN', password='YOUR PASSWORD')
    print('Authorizing...')
    vk.auth()
    print('Done.')
    AudioBOX.init()
