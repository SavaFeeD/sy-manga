import requests

from func.variable import Vars
from func.creator import FS
import json

# [PROFILE - USER] Parse (SAVE FROM SITE)
url = Vars().get_url('user')
folder = 'profile'
file = 'user'

parse_data = requests.get(url)
payload = {
    'content': parse_data.text,
    'folder': folder,
    'file': file
}
FS().save_data(payload)

# [PROFILE - USER] Load (GET FROM FILE)
payload = {
    'folder': folder,
    'file': file
}
data = FS().load_data(payload)

# [PROFILE - MANGA LIST] Parse (SAVE FROM SITE)
url = Vars().get_url('manga_list')
folder = 'profile'
file = 'manga_list'

parse_data = requests.get(url)
payload = {
    'content': parse_data.text,
    'folder': folder,
    'file': file
}
FS().save_data(payload)

# [PROFILE - USER] Load (GET FROM FILE)
payload = {
    'folder': folder,
    'file': file
}
data_ = FS().load_data(payload)
print(data_)
print('------------------------+------------------------')

# Parse manga pages and chapters href
FS().parse_manga_page({'data_': data_})
