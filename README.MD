# Mersenee Twister Challenge

### Understanding the code
The program first creates a random integer of length 32 bits and uses it to initialise a seed. The `getrandbit()` function then creates a random integer based on the seed. After that it creates 4 random numbers, and it **decrypts** the "[EXPLOIITM_MSG! ]..." message. Also another key thing to note is that the Initialisation Vector (IV) is the same as the Key. 

### Finding the first 4 numbers
To find the first 4 numbers, we can use the given ciphertext and the plaintext.
Let us split our ciphertext into 3 blocks of 16 bytes each. We can also observe that the first 1st and the 3rd block are the same.
Examining the AES encryption algorithm:
$ P_n = D(C_n) ⊕ C_n-1 $
Here $P_$n is the plaintext block, D() is the decrypt function, C_n is the nth ciphertext block. For $n=0$, $C_{n-1} = IV$

We also know that $C_0 = C_2$
Therefore:
$$P_0 = D(C_0) ⊕ IV \\
P_1 = D(C_1) ⊕ C_0 \\
P_2 = D(C_2) ⊕ C_1$$

We also know that $D(C_0) = D(C_2)$ and let us assume it is some X

$$
P_0 = X ⊕ IV \\
X = P_0 ⊕ IV \\
P_2 = X ⊕ C_1 \\
P_2 = P_0 ⊕ IV ⊕ C_1 \\
\\
IV = P_2 ⊕ P_0 ⊕ C_1$$

Once we have found the IV, we can find the key (since IV = Key) and then we can split the key into 4 parts of 4 bytes each and convert them to integers (minding the big endian format).

### Finding the seed
Now that we have the first 4 numbers, we can use those 4 numbers to find the seed using `this amazing github repository`. We will only use the `Breaker` class from `mersenne.py`. This class uses a minimum of 3 consecutive random numbers to find the seed. However we will use all 4 numbers here.
First we convert it to the format of `[(index, number)]` and we give it to the `Breaker()` class. Then we call the `get_seed_mt()` function to find the seed.

### After finding the seed
After finding the seed, we intiialise the random number generator, and after that we generate 4 numbers and recreate the key. Then we assert that the recreated key is the same as the key we found earlier to verify the `Breaker()` class worked correctly.
Finally we generate the next 8 numbers and convert them to bytes to get the actual key. We use that key to initialise the AES cipher and decrypt the final ciphertext to get the flag.

### Final output
The final output will be the time taken to complete the code and the flag 
```
[EXPLOIITM_MSG!]
d4pr0 is very impressed by your abilities. WhatsApp him "New phone who dis" and the SHA256 hash of your phone number. Good job
[EXPLOIITM_MSG!]
```
