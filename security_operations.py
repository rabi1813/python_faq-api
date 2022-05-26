"""
Security related operations
"""
import os
from common_utils import CommonUtilsMethods
from cryptography.fernet import Fernet


class SecurityMethods:
    """
    Security related methods
    """
    __slots__ = ()

    @staticmethod
    def generate_key_file(file_name):
        """
        Generates a key and save it into a file
        :param file_name: Name of secret key file name
        :return: None
        """
        dir_name = os.path.dirname(file_name)
        if dir_name != "":
            os.makedirs(dir_name, exist_ok=True)
        key = Fernet.generate_key()
        with open(file_name, "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(file_name):
        """
        Load the previously generated key
        :param file_name: Name of secret key file name
        :return: Secret key
        """
        return open(file_name, "rb").read()

    def encrypt_message(self, config_details, normal_string):
        """
        Encrypts a message
        :param config_details: Config File details
        :param normal_string: Normal String
        :return: Encrypted String
        """
        key = self.load_key(config_details.get("secret"))
        encoded_message = normal_string.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)
        encrypted_message = f.encrypt(encrypted_message)
        encrypted_message = f.encrypt(encrypted_message)

        return encrypted_message.decode()

    def decrypt_message(self, config_details, encrypted_message):
        """
        Decrypts an encrypted message
        :param config_details: Config File details
        :param encrypted_message: Encrypted String
        :return: Decrypted String
        """
        key = self.load_key(config_details.get("secret"))
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message.encode())
        decrypted_message = f.decrypt(decrypted_message)
        decrypted_message = f.decrypt(decrypted_message)

        return decrypted_message.decode()

    def decrypted_config(self):
        """
        Decrypt config data
        :return:Decrypted config data
        """
        config_data = CommonUtilsMethods.read_config_file()
        config_data["password"] = self.decrypt_message(config_data, config_data["password"])
        return config_data
