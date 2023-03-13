import random


def generate_key(list_characters=None, seed=0):
    if list_characters is None:
        list_characters = [char for char in range(5, 256)]
    random.seed(seed)
    random.shuffle(list_characters)
    return list_characters


def generate_int(num_digits):
    return int(random.random()*10**num_digits)


def encrypt(message, key, const, len_key):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.index(text[index_letter]) if text[index_letter] in key else -1
        if character >= 0:
            try:
                text[index_letter] = key[character+const+j]
            except IndexError:
                mod = (character + const + j) // len_key
                text[index_letter] = key[(character + const + j)-(len_key * mod)]
        j += const
    return bytearray(text)


def decrypt(message, key, const, len_key):
    text = list(message)
    j = 1
    for index_letter in range(len(text)):
        character = key.index(text[index_letter]) if text[index_letter] in key else -1
        if character >= 0:
            try:
                text[index_letter] = key[character - (const + j)]
            except IndexError:
                for i in range(len_key):
                    if (const + j + i) % len_key == character:
                        mod = (i + const + j) // len_key
                        text[index_letter] = key[(character + len_key * mod) - (const + j)]
                        break
        j += const
    return bytearray(text)
