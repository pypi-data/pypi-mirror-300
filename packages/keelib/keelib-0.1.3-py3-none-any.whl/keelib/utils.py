import numpy


def open_file(file_path):
    """
    Opens a file and reads its content as bytes.

    Args:
        file_path (str): The path to the file to open.

    Returns:
        bytes: The content of the file as bytes.
    """
    with open(file_path, "rb") as file:
        file_content = file.read()

    return file_content


def open_key(key_path):
    """
    Opens a key file and reads its content as a list of bytes.

    Args:
        key_path (str): The path to the key file to open.

    Returns:
        list: A list of bytes read from the key file.
    """
    key_instructions = []
    with open(key_path, "rb") as key:
        key = key.read()
        key_instructions = []
        for instruction in key:
            key_instructions.append(instruction)

    return key_instructions


def modify_file(list: bool, value, file_content=None, decrypt=False):
    """
    Modifies a file by adding or subtracting a value to/from each byte of the file.

    Args:
        list (bool): Whether the value is a list of bytes or a single byte.
        value (list or int): The value to add or subtract to/from each byte of the file.
        file_content (bytes): The content of the file as bytes. Defaults to None.
        decrypt (bool): Whether to subtract the value from the file content. Defaults to False.

    Returns:
        bytes: The modified content of the file as bytes.
    """

    new = []
    if list and not (decrypt):
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) + value[i]) % 0x100)
    elif list and decrypt:
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) - value[i]) % 0x100)
    elif not (list) and not (decrypt):
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) + value) % 0x100)
    elif not (list) and decrypt:
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) - value) % 0x100)
    file_content = bytearray(new)

    return file_content


def linear_gradient(key_instructions: list, file_content=None, decrypt=False):
    """
    Applies a linear gradient to the file content based on the key instructions.

    The gradient will go from the second value in the key instructions to the
    third value in the key instructions. If the length of the file content is
    zero, the gradient will be one step.

    Args:
        key_instructions (list): A list of bytes representing the key instructions.
        file_content (bytes): The content of the file as bytes. Defaults to None.
        decrypt (bool): Whether to subtract the gradient from the file content. Defaults to False.

    Returns:
        list: A list of two elements. The first element is the modified key instructions.
        bytes: The modified content of the file as bytes.
    """

    a, b = key_instructions[1], key_instructions[2]
    total_steps = len(file_content)

    steps_ab = int(round(total_steps))

    if steps_ab <= 0:
        steps_ab = 1

    gradient_ab = numpy.linspace(a, b, steps_ab, dtype=int)
    file_content = modify_file(True, gradient_ab, file_content, decrypt)

    return key_instructions, file_content


def gradient(key_instructions: list, file_content=None, decrypt=False):
    """
    Applies a gradient to the file content based on the key instructions.

    The gradient will go from the second value in the key instructions to the
    third value, then to the fourth value, and finally to the fifth value. If the
    length of the file content is zero, the gradient will be one step.

    Args:
        key_instructions (list): A list of bytes representing the key instructions.
        file_content (bytes): The content of the file as bytes. Defaults to None.
        decrypt (bool): Whether to subtract the gradient from the file content. Defaults to False.

    Returns:
        list: A list of two elements. The first element is the modified key instructions.
        bytes: The modified content of the file as bytes.
    """
    a, b, c, d = key_instructions[1], key_instructions[2], key_instructions[3], key_instructions[4]
    total_steps = len(file_content)

    diff_ab = b - a
    diff_bc = c - b
    diff_cd = d - c
    total_diff = diff_ab + diff_bc + diff_cd

    if total_diff <= 0:
        total_diff = 1
    exact_steps_ab = total_steps * diff_ab / total_diff
    exact_steps_bc = total_steps * diff_bc / total_diff
    exact_steps_cd = total_steps * diff_cd / total_diff

    steps_ab = int(round(exact_steps_ab))
    steps_bc = int(round(exact_steps_bc))
    steps_cd = total_steps - steps_ab - steps_bc

    if steps_ab <= 0:
        steps_ab = 1
        steps_bc = max(0, total_steps - steps_ab - steps_cd)
    if steps_bc <= 0:
        steps_bc = 1
        steps_cd = max(0, total_steps - steps_ab - steps_bc)
    if steps_cd <= 0:
        steps_cd = 1
        steps_bc = max(0, total_steps - steps_ab - steps_cd)

    gradient_ab = numpy.linspace(a, b, steps_ab, endpoint=False, dtype=int)
    gradient_bc = numpy.linspace(b, c, steps_bc, endpoint=False, dtype=int)
    gradient_cd = numpy.linspace(c, d, steps_cd, dtype=int)

    full_gradient = numpy.concatenate((gradient_ab, gradient_bc, gradient_cd))
    file_content = modify_file(True, full_gradient, file_content, decrypt)

    return key_instructions, file_content


def add(key_instructions: list, file_content=None, decrypt=False):
    """
    Adds a value to each byte of the file content.

    Args:
        key_instructions (list): A list of bytes representing the key instructions.
        file_content (bytes): The content of the file as bytes. Defaults to None.
        decrypt (bool): Whether to subtract the value from the file content. Defaults to False.

    Returns:
        list: A list of two elements. The first element is the modified key instructions.
        bytes: The modified content of the file as bytes.
    """
    file_content = modify_file(
        False, key_instructions[1], file_content, decrypt)

    return key_instructions, file_content


length = {
    0x23: 3,
    0x3f: 5,
    0xe4: 2
}
instructions = {
    0x23: linear_gradient,
    0x3f: gradient,
    0xe4: add
}
