# FLAG = os.environ.get("FLAG", "FMCTF{F4K3_FL49}").encode()
# key = os.urandom(7)
# encryptedFlag = xor(FLAG, key).hex()
# print(f"encryptedFlag = {encryptedFlag}")


    from pwn import *

    encryptedFlag = 'a850d725cb56b0de4fcb40de72a4df56a72ec06cafa75ecb41f51c95'

    cipher = bytes.fromhex(encryptedFlag)
    key = b""
    flag_format = b"FMCTF{"

    for i in range (len(flag_format)):
        key += bytes([cipher[i] ^ flag_format[i]])

    key += bytes([cipher[-1] ^ ord('}')])

    flag = xor(cipher,key)
    print(flag)

    # FMCTF{X0R_1S_L1K3_MAGIC_0x1}