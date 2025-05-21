import random
import socket
import time
import jwt
from qiskit import QuantumCircuit
from qiskit_aer import Aer, AerSimulator
from qiskit import transpile

n_qubits = 32
s_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
s_bits = [random.randint(0, 1) for _ in range(n_qubits)]

backend = Aer.get_backend('qasm_simulator')

HOST = '0.0.0.0'
PORT = 5001
SECRET_KEY = random.randbytes(16)
FLAG = "UMCS{<REDACTED>}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[+] Listening on port {PORT}...")

    conn, addr = server.accept()
    with conn:
        print(f"[+] Connection from {addr}")
        conn.sendall(b"Welcome to my bb84 simulator. This program will only transmit JWT tokens.\nSending qubits through quantum channel:\n")

        while True:
            r_bases = [random.choice(['Z', 'X']) for _ in range(n_qubits)]
            r_bits = []
            
            for i in range(n_qubits):
                qc = QuantumCircuit(1, 1)
                if s_bases[i] == 'Z':
                    if s_bits[i] == 1:
                        qc.x(0)
                else:
                    if s_bits[i] == 0:
                        qc.h(0)
                    else:
                        qc.x(0)
                        qc.h(0)

                if r_bases[i] == 'X':
                    qc.h(0)

                qc.measure(0, 0)

                new_cirq = transpile(qc, backend)
                job = backend.run(new_cirq)
                counts = job.result().get_counts()
                measured_bit = int(list(counts.keys())[0])
                r_bits.append(measured_bit)

            xor = [s_bits[i] ^ r_bits[i] for i in range(n_qubits)]

            for i in range(n_qubits):
                basis_a = s_bases[i].lower()
                basis_b = r_bases[i].lower()
                qwt = {"basis_a": basis_a, "basis_b": basis_b, "xor": xor[i]}
                qwt = jwt.encode(qwt, SECRET_KEY, algorithm="HS256")
                conn.sendall(qwt.encode() + b"\n")
                time.sleep(0.5)

            key_bits = []
            key_indices = []
            for i in range(n_qubits):
                if s_bases[i] == r_bases[i]:
                    key_bits.append(s_bits[i])
                    key_indices.append(i)

            p_key = {i: key_bits[j] for j, i in enumerate(key_indices)}
            conn.sendall(jwt.encode(p_key, SECRET_KEY, algorithm="HS256").encode() + b"\n")
            conn.sendall(b"Do you want somemore tokens? (y/n): ")
            response = conn.recv(1024).decode().strip().lower()
            if response != 'y':
                break

        conn.sendall(b"Guess Bob's qubits (comma as delimeter): ")
        guess = conn.recv(4096).decode().strip()
        try:
            guess_bits = list(map(int, guess.split(',')))
            if guess_bits == r_bits:
                conn.sendall(b"\033[32;1mFLAG: " + FLAG.encode() + b"\033[0m\n")
            else:
                conn.sendall(b"\033[31;1mFLAG: You have the worst guess ever.\033[0m\n")
        except:
            conn.sendall(b"Invalid input format.\n")

        print("[+] Connection closed.")
        conn.close()
