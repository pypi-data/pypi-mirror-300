# Kelian

Kelian is a Python library that provides a collection of useful and commonly used code snippets to speed up development and avoid reinventing the wheel. It includes utility functions, common algorithms, data manipulations, and more, designed to simplify your workflow and increase productivity.

## Features

- **Encryption Utilities**: Simple functions to encrypt and decrypt data using predefined mappings or lists.
- **System Information**: Retrieve detailed information about your computer's hardware, including processor, motherboard, GPU, RAM, and more.
- **Utilities**: Helper functions like hashing utilities for common tasks.

## Installation

You can install the Kelian library via pip:

```bash
pip install kelian
```

## Usage

### Example 1: Encryption Functions

```python
from kelian import encrypt, decrypt

# Encrypt a string
encrypted_text = encrypt("Hello")
print(encrypted_text)

# Decrypt the string
decrypted_text = decrypt(encrypted_text)
print(decrypted_text)
```

### Example 2: System Information Retrieval

```python
from kelian import get_processor_details, get_ram_details

# Get processor details
processor_info = get_processor_details()
print(processor_info)

# Get RAM details
ram_info = get_ram_details()
print(ram_info)
```

### Example 3: Utilities

```python
from kelian import string2hash

# Generate a hash from a string
hashed_string = string2hash("password123")
print(hashed_string)
```

## Functions

### Encryption Functions

- `alpha2dict()`: Maps alphabets to a dictionary for encryption.
- `list2dict()`: Converts a list to a dictionary.
- `encrypt(text)`: Encrypts a given text using predefined mappings.
- `decrypt(text)`: Decrypts a given encrypted text.
- `encrypt_by_list(text, lst)`: Encrypts text based on a custom list.
- `decrypt_by_list(text, lst)`: Decrypts text based on a custom list.

### System Functions

- `get_processor_details()`: Returns details about the CPU.
- `get_motherboard_details()`: Returns details about the motherboard.
- `get_gpu_details()`: Returns details about the GPU.
- `get_monitor_details()`: Returns details about the monitor.
- `get_cd_drive_details()`: Returns details about the CD drive.
- `get_mouse_details()`: Returns details about the mouse.
- `get_speaker_details()`: Returns details about the speakers.
- `get_keyboard_details()`: Returns details about the keyboard.
- `get_hard_disk_details()`: Returns details about the hard disk.
- `get_ram_details()`: Returns details about the RAM.

### Utility Functions

- `string2hash(text)`: Converts a string to its hashed value.

## License

This project is licensed under the MIT License. See the <a href="./LICENSE.txt">LICENSE</a> file for more details.
