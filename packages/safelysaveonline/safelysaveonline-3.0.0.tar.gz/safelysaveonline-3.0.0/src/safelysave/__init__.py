import os
import shutil
import json
import uuid

from cryptography.fernet import Fernet
import git

def create_sso_file(location: str, server_type: str, server_address: str) -> bytes:
    content: dict = {
        'data': [],
        'additions': [],
        'removals': [],
        'server_type': server_type,
        'server_address': server_address,
        'file_uuid': str(uuid.uuid4())
    }

    key: bytes = Fernet.generate_key()
    enc = Fernet(key)

    content_json: str = json.dumps(content)
    content_enc: bytes = enc.encrypt(content_json.encode())

    with open(location, 'wb') as file:
        file.write(content_enc)
    return key

class sso:
    def __init__(self, location: str, key: bytes) -> None:
        self.location = location
        self.key = key

        try:
            enc = Fernet(key)
        except:
            raise Exception("Invalid key / Something went wrong")

        try:
            with open(location, 'rb') as file:
                content_enc: bytes = file.read()

            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)
        except:
            raise Exception("Failed loading file")

    def get_data(self) -> list:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            data: list = content['data']
            additions: list = content['additions']
            removals: list = content['removals']

            for i in range(len(additions)):
                data.append(additions[i])

            for i in range(len(removals)):
                for j in range(len(data)):
                    if data[j]['uuid'] == removals[i]:
                        del data[j]
                        break

            return data
        else:
            data = []
            return data

    def add_data(self, data: dict) -> None:
        if os.path.isfile(self.location) == True:
            data['uuid'] = str(uuid.uuid4())

            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content['additions'].append(data)

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)

    def remove_data(self, data_uuid: str) -> None:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content['removals'].append(data_uuid)

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)

    def sync(self) -> None:
        with open(self.location, 'rb') as file:
            content_enc: bytes = file.read()

        enc = Fernet(self.key)
        content_json: str = enc.decrypt(content_enc).decode()
        content: dict = json.loads(content_json)

        if os.path.exists('sso-temp-repo') == True:
            shutil.rmtree('sso-temp-repo')

        if content['server_type'] == 'git':
            repo = git.Repo.clone_from(content['server_address'], 'sso-temp-repo')
            repo = git.Repo('sso-temp-repo')
            os.chdir('sso-temp-repo')

            file_path = content['file_uuid'] + '.sso'
            if os.path.isfile(file_path) == True:
                with open(file_path, 'rb') as file:
                    content_enc = file.read()
                content_json: str = enc.decrypt(content_enc).decode()
                content_of_file_in_repo: dict = json.loads(content_json)
                content['data'] = content_of_file_in_repo['data']

            data: list = content['data']
            additions: list = content['additions']
            removals: list = content['removals']

            for i in range(len(additions)):
                data.append(additions[i])

            for i in range(len(removals)):
                for j in range(len(data)):
                    if data[j]['uuid'] == removals[i]:
                        del data[j]
                        break

            content['data'] = data
            content['additions'] = []
            content['removals'] = []

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)

            with open(file_path, 'wb') as file:
                file.write(content_enc)

            repo.index.add([file_path])
            commit_message = '[SSO] Synced data of profile ' + content['file_uuid'] + ' with client.'
            repo.index.commit(commit_message)

            origin = repo.remote(name='origin')
            origin.push()

            if os.path.isdir('../sso-temp-repo') == True:
                shutil.rmtree('../sso-temp-repo')

    def overrite_file(self, name: str, value) -> None:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content[name] = value

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)
