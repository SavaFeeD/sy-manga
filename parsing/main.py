import requests

from func.variable import Vars
from func.creator import FS


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

payload = {
    'folder': folder,
    'file': file
}
data = FS().load_data(payload)
print(data)
