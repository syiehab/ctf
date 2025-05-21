from pwn import remote
import jwt

# Configuration
HOST = "116.203.176.73"  # or actual IP/hostname
PORT = 5001
n_qubits = 32

# Tracking known bits from p_key
known_s_bits = {}

# Connect to server
r = remote(HOST, PORT)
print(r.recvuntil(b'Sending qubits through quantum channel:\n').decode())

while len(known_s_bits) < n_qubits:
    jwt_lines = []

    # Read 32 JWTs + 1 p_key JWT
    for _ in range(n_qubits + 1):
        line = r.recvline().strip().decode()
        jwt_lines.append(line)

    # Decode p_key and update known_s_bits
    p_key = jwt.decode(jwt_lines[-1], options={"verify_signature": False})
    for i, bit in p_key.items():
        known_s_bits[int(i)] = bit

    print(f"[+] Collected {len(known_s_bits)} known s_bits.")
    if len(known_s_bits) == n_qubits:
        r.recvuntil(b"Do you want somemore tokens? (y/n): ")
        r.sendline(b'n')
        break

    r.recvuntil(b"Do you want somemore tokens? (y/n): ")
    r.sendline(b'y')

# Now reconstruct r_bits from xor = s_bit ^ r_bit
r_bits = []
for i in range(n_qubits):
    token = jwt_lines[i]
    data = jwt.decode(token, options={"verify_signature": False})
    xor_bit = data['xor']
    s_bit = known_s_bits[i]
    r_bit = xor_bit ^ s_bit
    r_bits.append(str(r_bit))

# Send the guess
r.recvuntil(b"Guess Bob's qubits (comma as delimeter): ")
guess_string = ",".join(r_bits)
r.sendline(guess_string.encode())

# Receive FLAG
print(r.recvall(timeout=5).decode())
