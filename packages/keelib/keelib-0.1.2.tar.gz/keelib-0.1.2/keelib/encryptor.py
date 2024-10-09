from .utils import *


class Encryptor:
    def __init__(self, key_path):
        self.key_path = key_path

    def encrypt_file(self, file_path, output_path):
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
