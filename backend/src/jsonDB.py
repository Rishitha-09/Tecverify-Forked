import os
import json

from genericDB import Generic_DB

class JSON_DB(Generic_DB):

    def __init__(self, idGenerator_obj, crypt_obj, file: str) -> None:
        self.idGenerator_obj = idGenerator_obj
        self.crypt_obj = crypt_obj
        self.file = file


    def create_empty_json_file(self) -> bool:
        """
        This method creates empty JSON file 
        """
        try:
            default_data = []
            self.write(default_data)
            return True
        except Exception as e:
            print("\nException in create_empty_json_file(): ", e)
            return False


    def read(self):
        try:
            if not os.path.isfile(self.file) or os.stat(self.file).st_size == 0:
                self.create_empty_json_file()
            with open(self.file, 'r') as fHandle:
                secrets = json.load(fHandle)
            return secrets
        except Exception as e:
            print("\nException in read(): ", e)
            return None


    def write(self, data) -> bool:
        try:
            with open(self.file, 'w') as fHandle:
                json.dump(data, fHandle, indent=4)
            return True
        except Exception as e:
            print("\nException in write(): ", e)
            return False


    def delete_secret(self, secret_id) -> bool:
        secrets_list = self.read()
        for secret in secrets_list:
            if secret_id in secret.values():
                secrets_list.remove(secret)
                self.write(secrets_list)
                return True


    def auto_save_secret(self, okta_shared_secret, okta_logged_in_user_id, okta_logged_in_username, okta_factor_id) -> bool:
        secretInfo = self.prepare_secret_dictionary_for_auto_save_secret(okta_shared_secret, okta_logged_in_user_id, okta_logged_in_username, okta_factor_id)
        secrets_list = self.read()
        secrets_list.append(secretInfo)
        return self.write(secrets_list)


    def manual_save_secret(self, form_data, okta_logged_in_user_id) -> bool:
        secretInfo = self.prepare_secret_dictionary_for_manual_save_secret(form_data, okta_logged_in_user_id)
        secrets_list = self.read()
        secrets_list.append(secretInfo)
        return self.write(secrets_list)