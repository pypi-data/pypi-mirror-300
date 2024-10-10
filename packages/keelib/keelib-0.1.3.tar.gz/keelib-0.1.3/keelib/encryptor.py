from .utils import *


class Encryptor:
    """
    A class for encrypting and decrypting files using a key file.

    Attributes:
        key_path (str): The path to the key file to use for encryption and decryption.

    Methods:
        encrypt_file(file_path, output_path): Encrypts a file using the key file and saves the result to the specified path.
        decrypt_file(file_path, output_path): Decrypts a file using the key file and saves the result to the specified path.
    """

    def __init__(self, key_path):
        self.key_path = key_path

    def encrypt_file(self, file_path, output_path):
        """
        Encrypts a file using the key file and saves the result to the specified path.

        Args:
            file_path (str): The path to the file to encrypt.
            output_path (str): The path to save the encrypted file to.

        Returns:
            None
        """
        instructions_left = True
        file_content = open_file(file_path)
        key_instructions = open_key(self.key_path)

        while instructions_left:
            key_instructions, file_content = instructions[key_instructions[0]](
                key_instructions, file_content, False)
            for instruction in range(0, length[key_instructions[0]]):
                key_instructions.pop(0)
            if not len(key_instructions) > 0:
                instructions_left = False

        with open(output_path, "wb") as file:
            file.write(file_content)

        file.close()

    def decrypt_file(self, file_path, output_path):
        """
        Decrypts a file using the key file and saves the result to the specified path.

        Args:
            file_path (str): The path to the file to decrypt.
            output_path (str): The path to save the decrypted file to.

        Returns:
            None
        """
        instructions_left = True
        file_content = open_file(file_path)
        key_instructions = open_key(self.key_path)

        while instructions_left:
            key_instructions, file_content = instructions[key_instructions[0]](
                key_instructions, file_content, True)
            for instruction in range(0, length[key_instructions[0]]):
                key_instructions.pop(0)
            if not len(key_instructions) > 0:
                instructions_left = False

        with open(output_path, "wb") as file:
            file.write(file_content)

        file.close()
