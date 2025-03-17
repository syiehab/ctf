from functions import *
from pwn import remote
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import unhexlify

r = remote('superguesser.fmc.tf',2002)

r.recvuntil(b' flag: \n')
enc_flag = r.recvline().strip().decode()

print(f'Encrypted flag: {enc_flag}')

hints = []
index = [3, 4, 5, 6, 230, 231, 232, 233]
for i in index:
    r.recvuntil(b'Enter an index (0-624): ')
    r.sendline(str(i).encode())
    r.recvuntil(b': ')
    hint = int(r.recvline().strip().decode())
    hints.append(hint)

print(f"Hints: {hints}\n")

S = [untemper(hint) for hint in hints]

I_230_, I_231 = invertStep(S[0], S[4])
I_231_, I_232 = invertStep(S[1], S[5])
I_232_, I_233 = invertStep(S[2], S[6])
I_233_, I_234 = invertStep(S[3], S[7])

I_231 += I_231_
I_232 += I_232_
I_233 += I_233_

seed_l = recover_Kj_from_Ii(I_233, I_232, I_231, 233) - 16

seed_h1 = recover_Kj_from_Ii(I_234, I_233, I_232, 234) - 17
seed_h2 = recover_Kj_from_Ii(I_234+0x80000000, I_233, I_232, 234) - 17

seed1 = (seed_h1 << 32) + seed_l
seed2 = (seed_h2 << 32) + seed_l

seedA = bytes.fromhex(hex(seed1)[2:])
seedB = bytes.fromhex(hex(seed2)[2:])

seeds = [seedA, seedB]

def encrypt_flag(flag, iv):
    key = random.getrandbits(128).to_bytes(16, 'big')
    cipher = AES.new(key, AES.MODE_CBC, iv*2)
    encrypted = cipher.encrypt(pad(flag.encode(), AES.block_size))
    print(f"Key: {key.hex()}")
    print(f"IV: {(iv*2).hex()}")
    return encrypted, unhexlify(key.hex())

for seed in seeds:
    print(f"Using seed: {seed}")
    random.seed(seed)
    hints = [random.getrandbits(32) for _ in range(624)]
    encrypted, key = encrypt_flag("flag{testflag}", seed)
    iv = unhexlify((seed * 2).hex())
    enc = unhexlify(enc_flag)

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_flag = unpad(cipher.decrypt(enc), AES.block_size).decode()
        print("Success!")
        print(f"Decrypted Flag: {decrypted_flag}")
        break
    except:
        print("Failed!")
        print()
    continue

# Encrypted flag: 00f1fc6e6076bc825c9bd883687f7f046d037a6b1fb69897b2fb4eded5c62dc555864c44030dff237c12fd372f5b16b6
# Hints: [2725780700, 770060442, 2410503287, 1509336382, 83677964, 3230463657, 3717655272, 2922929094]

# Using seed: b'\xa8%\x94\xac\xee\x99\xd7O'
# Key: ede5d9661b2700f9a5fc3e3baf8ac030
# IV: a82594acee99d74fa82594acee99d74f
# Success!
# Decrypted Flag: FMCTF{V2_MT19937_S33d_Unc0v3r3d}
