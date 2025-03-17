from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from math import gcd
from gmpy2 import isqrt


pem_key = """-----BEGIN PUBLIC KEY-----
MIGcMA0GCSqGSIb3DQEBAQUAA4GKADCBhgKBgGjpRi/Hr5oN5NS219dZrq6nW7AC
Y7fUItXAvbgy0TtagVKO2goQiOssL331b7zRjMvdHkEBR4bTd+hHblmynO+2//fz
4DmVgdgMnrP54+2RSzguEGS1ONX4MpJonBsEGGc1IOiKECiwIbl4DkyTxl6AnFsz
ZI2E+lLDZnX5P44FAgEQ
-----END PUBLIC KEY-----"""

rsa_key = RSA.import_key(pem_key)

n = rsa_key.n
e = rsa_key.e
cipher =  b'\x10\xc4\xbf\xfapg\xee\x00\xe4\xcd\x00\xb4i\xf5\x801\xdd\xafm\xb1\xad\x8dy\x01\xaa\x14\xd1\xa3\x14[\xdf\xc8c\xb1\xf4\xcb\xcf\xf0\xf9\x83\x85%\x19\xd2d>N\x9aR\xa4\xba\xc9\xda\xd8\xe4\xa2\x9cg%.\xac\xd7\xb5\x95\x7f\x87\x04?\xf7\xe4\x06(\xe7l\x1c"c\x95\x90z\xd4\x8b\x9f\x1b\x00\xc67\xe4\x82g\xc4b\x10\x8c\xe7s[\x95-TB+Z;\xe4\x00\x11<\xc51K\xec\x94ZL\xb2\xf9\x7fp<\xe6C\xf8\x7f\x90\x0bG\xcf'
c = bytes_to_long(cipher)

print(f"n: {n}")
print(f"e: {e}")

a = isqrt(n) + 1
b2 = a*a - n
while not isqrt(b2)**2 == b2:
    a += 1
    b2 = a*a - n

b = isqrt(b2)
p = a - b
q = a + b

print(f"p: {p}")
print(f"q: {q}")

def find_roots_of_unity(n, e, max_roots=10):
    phi_n = (p-1)*(q-1)  
    k = gcd(e, phi_n) 
    
    if k == 1:
        print("No nontrivial roots exist.")
        return []

    roots = []
    for a in range(1, max_roots + 1):  
        r = pow(a, phi_n // k, n)  
        if pow(r, e, n) == 1:  
            roots.append(r)

    return roots

def recover_plaintexts(c, n, e):
    phi_n = (p-1)*(q-1)
    k = gcd(e, phi_n)

    if k == 1:
        print("No valid decryption possible.")
        return []

    d = pow(e, -1, phi_n // k)
    g = pow(c, d, n) 

    roots = find_roots_of_unity(n, e)
    plaintexts = [g * l % n for l in roots] 

    return plaintexts


plaintexts = recover_plaintexts(c, n, e)

for pt in plaintexts:
    try:
        decoded = long_to_bytes(pt)
        if b'FMCTF' in decoded:
            print(f"{decoded}")
    except:
        print("Failed to decode")

# n: 73671169113692412161518091695991074472499960503340036931063401833844789007180020715886458582760614423768286510200921468682879797651585778343666370976746242033960964171883195866661042323420463092656546940842903827382288624493399406855771112920858499309807681038473688274738183488216155275283711673441904987653
# e: 16
# p: 8583191079877717143954293663418499797265896659440705659861607727231607813990404415197156190837935083515591819471515635634480053063098019015612140184864883      
# q: 8583191079877717143954293663418499797265896659440705659861607727231607813990404415197156190837935083515591819471515635634480053063098019015612140184865191      
# b'FMCTF{S0lv3d_w1th_R4b1n_fx777}'