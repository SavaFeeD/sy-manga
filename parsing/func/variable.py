class Vars:
    def __init__(self):
        self.api = 'https://api.remanga.org/api'
        self.web = 'https://remanga.org'
        self.my_id = 146493
        self.web_keys = {
            'chapter': {
                'href_1': '/manga/',
                'href_2': '/ch'
            }
        }
        self.urls = {
            'user': f'{self.api}/users/{self.my_id}',
            'manga_list': f'{self.api}/users/{self.my_id}/bookmarks/?type=0&count=24&page=1'
        }

    def get_url(self, url_name):
        return self.urls[url_name]

    def get_chapters_attr_href(self, dir_name):
        return f'{self.web_keys["chapter"]["href_1"]}{dir_name}{self.web_keys["chapter"]["href_2"]}'
