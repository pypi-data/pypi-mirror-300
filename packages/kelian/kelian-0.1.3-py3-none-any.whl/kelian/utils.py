import hashlib

def string2hash(input_string:str, algorithm:str='sha256') -> str:
    # Crée un nouvel objet de hash avec l'algorithme spécifié
    hash_function = hashlib.new(algorithm)
    # Met à jour l'objet de hash avec la chaîne de caractères (en encodage binaire)
    hash_function.update(input_string.encode('utf-8'))
    # Renvoie la chaîne de caractères hachée sous forme hexadécimale
    return hash_function.hexdigest()
