# __init__.py

"""
kelian: Une bibliothèque Python de bout de code utiles
-----------------------------------------------------
Description:
    Cette bibliothèque permet d'être plus rapide dans le développement Python en évitant de réinventer la roue.
    Elle est composée de nombreux bouts de code couramment utilisés, tels que des fonctions d'utilitaires, des 
    algorithmes classiques, des manipulations de données, et bien plus encore, afin de simplifier le développement
    et améliorer la productivité.

Auteur:
    Kelian

Licence:
    MIT License (voir LICENSE pour plus de détails)

Version:
    0.1.0
"""

__version__ = "0.1.3"
__author__ = "Kelian"
__license__ = "MIT"

from .encryption import alpha2dict, list2dict, encrypt, decrypt, encrypt_by_list, decrypt_by_list, encrypt_by_character_manga, decrypt_by_character_manga
from .system import get_processor_details, get_motherboard_details, get_gpu_details, get_monitor_details, get_cd_drive_details, get_mouse_details, get_speaker_details, get_keyboard_details, get_hard_disk_details, get_ram_details
from .utils import string2hash

# Définir ce qui sera importé lors d'un 'from package import *'
__all__ = [
    "alpha2dict", 
    "list2dict", 
    "encrypt", 
    "decrypt", 
    "encrypt_by_list", 
    "decrypt_by_list", 
    "encrypt_by_character_manga", 
    "decrypt_by_character_manga", 
    "get_processor_details", 
    "get_motherboard_details", 
    "get_gpu_details", 
    "get_monitor_details", 
    "get_cd_drive_details", 
    "get_mouse_details", 
    "get_speaker_details", 
    "get_keyboard_details", 
    "get_hard_disk_details", 
    "get_ram_details", 
    "string2hash"
]
