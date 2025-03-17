flag = "FMCTF{REDACTED}"
flag = ''.join(['F', 'M', 'C', 'T', 'F', '{', 'u', 'o', '~', 'b', '}', 'V', '{', 'Q'])
flag += '_' * (len(flag) - 37)
flag += '}'
print(flag)

def enc(data : str):
    result = []
    for i in range(len(data)):
        result.append(((ord(data[i - 1]) + ord(data[i]) + ord(data[(i + 1) % len(data)])) % 256).to_bytes())
                
    return b''.join(result)
print(enc(flag))
open("./flag3.enc", "wb").write(enc(flag))

