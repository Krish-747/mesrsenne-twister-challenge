import random

import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

# Some one told me python's rng is insecure so I'm using Numpy :)
np.random.seed(s := random.getrandbits(32))


def getrandbits(bits):
    return np.random.randint(0, 2**bits)


key = b""
for i in range(4):
    key += long_to_bytes(a := getrandbits(32)).zfill(4)
not_secret_message = b"[EXPLOIITM_MSG!]d4pr0,says_Hallo[EXPLOIITM_MSG!]"

# Wt is an initialisation vector anyway?
aes = AES.new(key, AES.MODE_CBC, iv=key)

# Oops a typo, shouldn't matter too much should it?
h = aes.decrypt(not_secret_message).hex()

# You can have the not secret message
print(h)
print("=" * 32)

key1 = b""
for i in range(8):
    key1 += long_to_bytes(a := getrandbits(32)).zfill(4)


secret_message = b"(HIDDEN)"

aes_ = AES.new(key1, AES.MODE_ECB)
h1 = aes_.encrypt(secret_message).hex()
print(h1)
