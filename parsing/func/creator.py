import os
import json
import bz2


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
        path = f'{self.base_path}\{payload["folder"]}\{payload["file"]}.cpd'

        # Decompress
        with bz2.open(path, "rb") as fin:
            data = fin.read()

        # Decoding
        data = json.loads(data)

        return data
