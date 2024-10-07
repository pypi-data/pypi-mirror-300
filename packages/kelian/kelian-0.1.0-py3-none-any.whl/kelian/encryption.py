import random

ALPHA = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789éêï~\"#'{([-|è`_\çà@)]=}°/*+<>?,.;:§!¨^¤£$€µ%ù²& \n"
ALPHA_HEX = "0123456789abcdef"

def alpha2dict(x:str) -> dict:
    return {
        list(x)[i]:[i+1 for i in range(len(list(x)))][i]
        for i in range(len(list(x)))
    }

def list2dict(list_:list[str], alpha:str=ALPHA_HEX):
    data_alpha = {k:[] for k in alpha}
    data_list_ = {k:[] for k in list_}

    if len(alpha) < len(list_):
        alpha *= (len(list_) // len(alpha)) + 1
        alpha = alpha[:len(list_)]
    else:
        list_ *= (len(alpha) // len(list_)) + 1
        list_ = list_[:len(alpha)]

    for index in range(len(alpha)):
        data_alpha[alpha[index]].append(list_[index])

    for index in range(len(list_)):
        data_list_[list_[index]].append(alpha[index])
    
    return data_alpha, data_list_

def encrypt(message:str, password:str, alpha:str=ALPHA) -> str:
    message = message.encode('utf-8').hex()
    dictionaire = alpha2dict(alpha)
    Int_Message, Int_MDP, Int_Token, Str_Token = [], [], [], []
    while len(list(message)) > len(list(password)): password = password + password
    for i in range(len(password)): Int_MDP.append(dictionaire[password[i]])
    for i in range(len(message)): Int_Message.append(dictionaire[message[i]])
    for i in range(len(message)): Int_Token.append(Int_Message[i] + Int_MDP[i])
    for i in range(len(Int_Token)):
        if Int_Token[i] > len(list(alpha)): Str_Token.append(str(list(dictionaire.keys())[list(dictionaire.values()).index(Int_Token[i]-len(list(alpha)))]))
        else: Str_Token.append(str(list(dictionaire.keys())[list(dictionaire.values()).index(Int_Token[i])]))
    return "".join(Str_Token)

def decrypt(message:str, password:str, alpha:str=ALPHA) -> str:
    dictionaire = alpha2dict(alpha)
    Int_Message, Int_MDP, Int_Token, Message = [], [], [], []
    while len(list(message)) > len(list(password)): password = password + password
    for i in range(len(password)): Int_MDP.append(dictionaire[password[i]])
    for i in range(len(message)): Int_Token.append(dictionaire[message[i]])
    for i in range(len(message)): Int_Message.append(Int_Token[i] - Int_MDP[i])
    for i in range(len(Int_Message)):
        if Int_Message[i] <= 0: Message.append(list(dictionaire.keys())[list(dictionaire.values()).index(Int_Message[i]+len(alpha))])
        else: Message.append(list(dictionaire.keys())[list(dictionaire.values()).index(Int_Message[i])])
    return bytes.fromhex("".join(Message)).decode()

def encrypt_by_list(message:str, password:str, list_:list[str], sep:str="") -> str:
    data, _ = list2dict(list_, ALPHA_HEX)
    password = password.encode('utf-8').hex()
    return sep.join([
        random.choice(data[char]) 
        for char in list(encrypt(message, password, ALPHA_HEX))
    ])

def decrypt_by_list(message:str, password:str, list_:list[str], sep:str="") -> str:
    _, data = list2dict(list_, ALPHA_HEX)
    password = password.encode('utf-8').hex()
    return decrypt("".join([
        data[char][0] 
        for char in message.split(sep)
    ]), password, ALPHA_HEX)
