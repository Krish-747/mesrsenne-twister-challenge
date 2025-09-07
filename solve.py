import binascii
from mersenne import *
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
import random
import numpy as np


example_ciphertext = b"[EXPLOIITM_MSG!]d4pr0,says_Hallo[EXPLOIITM_MSG!]"
example_decrypted = b"b2d706867f5cc98996d1eb8c8ca50c90aff544d5ebb1bec420e1608665f087ad729c62a071fb570fc9286ce9cee4988e"
actual_encrypted = b"2ba110f444185dcf71879fd17460ca2a5cce3457cdb922738ec87d3deac9aee1a386dd6a62df82a2563313551ec13f487391915d9031f37329c5b0c350254cc7634a0f05b1557b681cf06a926e602071e600fd198523d001e451ae41eca7da41ab5951acbc205983a0759ca0bddebbc85c41207e5cd4462188154a66155f482e10f52634ed8f5de861a74b4e04841bd32ba110f444185dcf71879fd17460ca2a"

example_decrypted = binascii.unhexlify(example_decrypted)
actual_encrypted = binascii.unhexlify(actual_encrypted)

middle_ciphertext = example_ciphertext[16:32]
first_decrypted = example_decrypted[:16]
third_decrypted = example_decrypted[32:48]

key = bytes([a ^ b ^ c for a, b, c in zip(
    first_decrypted, third_decrypted, middle_ciphertext)])

first_four_numbers = []
for i in range(4):
    part = key[(4*i):4*(i+1)]
    val = int.from_bytes(part, 'big')
    first_four_numbers.append((i, val))

b = Breaker()
recovered_seed = b.get_seed_mt(first_four_numbers)

# Getting the keys from the recovered seed
np.random.seed(s := recovered_seed)

def getrandbits(bits):
    return np.random.randint(0, 2**bits)

#Regenerating the intial 4 keys
test_key = b""
for i in range(4):
    test_key += long_to_bytes(a := getrandbits(32)).zfill(4)

assert test_key==key

#Getting the keys we actually need
actual_key = b""
for i in range(8):
    actual_key += long_to_bytes(a := getrandbits(32)).zfill(4)

#Decrypting the actual message
aes_ = AES.new(actual_key, AES.MODE_ECB)
h1 = aes_.decrypt(actual_encrypted).decode()
print(h1)
