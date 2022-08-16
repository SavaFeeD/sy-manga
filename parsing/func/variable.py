class Vars:
    variable = {
        'api': 'https://api.remanga.org/api',
        'web': 'https://remanga.org',
        'my_id': 146493,
    }
    urls = {
        'user': f'{variable["api"]}/users/{variable["my_id"]}'
    }

    def get_var(self, name):
        return self.variable[name]

    def get_url(self, name):
        return self.urls[name]
