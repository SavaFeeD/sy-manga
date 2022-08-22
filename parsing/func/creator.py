import os
import re
import json
import bz2
import requests
from bs4 import BeautifulSoup

from func.variable import Vars


def create_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            print("Создать директорию %s не удалось" % path)
        else:
            print("Успешно создана директория %s" % path)


class FS:

    def __init__(self):
        self.base_path = os.path.abspath(__file__).split('\ '[0])
        self.base_path = self.base_path[:len(self.base_path) - 2]
        self.base_path = '\ '[0].join(self.base_path)
        self.base_path = f'{self.base_path}\data'

    def save_data(self, payload):
        # +-----------------------------------------------------------------+
        # |                         PAYLOAD                                 |
        # +-----------------------------------------------------------------+
        # |  folder        |     name dir                                   |
        # |  file          |     name file                                  |
        # |  content       |     data put in file                           |
        # +-----------------------------------------------------------------+

        folder_path = f'{self.base_path}\{payload["folder"]}'
        file_path = f'{folder_path}\{payload["file"]}.cpd'

        # Create directory
        create_dir(folder_path)

        # Encoding
        with open(file_path, 'w') as f:
            json.dump(payload['content'], f)

        # Compress
        with open(file_path, mode="rb") as fin:
            compress_data = fin.read()
            with bz2.open(file_path, "wb") as fout:
                fout.write(compress_data)

    def load_data(self, payload):
        # +-----------------------------------------------------------------+
        # |                         PAYLOAD                                 |
        # +-----------------------------------------------------------------+
        # |  folder        |     name dir                                   |
        # |  file          |     name file                                  |
        # +-----------------------------------------------------------------+

        path = f'{self.base_path}\{payload["folder"]}\{payload["file"]}.cpd'

        # Decompress
        with bz2.open(path, "rb") as fin:
            data = fin.read()

        # Decoding
        data = json.loads(json.loads(data))

        return data

    def manga_page_save_and_get_chapters_href(self, payload):
        # +-----------------------------------------------------------------+
        # |                         PAYLOAD                                 |
        # +-----------------------------------------------------------------+
        # |  url           |     [web] url manga in site                    |
        # |  folder        |     name manga (dir)                           |
        # |  file          |     name html file with manga page             |
        # +-----------------------------------------------------------------+

        folder_path = f'{self.base_path}\{payload["folder"]}'
        file_path = f'{folder_path}\{payload["file"]}.html'

        chapters_href = Vars().get_chapters_attr_href(payload["folder"])

        r = requests.get(payload['url'])
        soup = BeautifulSoup(r.text, file_path)

        all_a = soup.find_all("a", href=re.compile(chapters_href))
        list_href = []
        if all_a:
            for a in all_a:
                print(a["href"])
                list_href.append(a["href"])

        print(list_href)
        payload_href = {
            'folder': f'manga_chapters_list\{payload["file"]}',
            'file': payload["file"],
            'content': list_href
        }
        self.save_data(payload_href)
        return list_href

    def parse_manga_page(self, payload):
        # +-----------------------------------------------------------------+
        # |                         PAYLOAD                                 |
        # +-----------------------------------------------------------------+
        # |  data_           |     data with getting load profile           |
        # |                  |     manga list                               |
        # +-----------------------------------------------------------------+

        data_ = payload['data_']
        list_manga = []

        for manga in data_['content']:
            schema = {
                'url': f'{Vars().web}/manga/{manga["title"]["dir"]}?subpath=content',
                'folder': 'manga_pages',
                'file': manga["title"]["dir"]
            }
            list_manga.append(schema)

        for manga in list_manga:
            self.manga_page_save_and_get_chapters_href(manga)
