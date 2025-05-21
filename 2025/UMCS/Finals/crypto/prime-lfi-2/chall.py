    from Crypto.Util.number import isPrime, bytes_to_long
    from sage.all import *
    import socket
    import multiprocessing
    import sys

    FLAG = b'UMCS{<REDACTED>}'
    HOST = '0.0.0.0'
    PORT = 5002

    def send_points(p, a, b, q):
        E1 = EllipticCurve(GF(p), [a, b])
        E2 = EllipticCurve(GF(q), [a, b])

        m1, m2 = bytes_to_long(FLAG[:len(FLAG)//2]), bytes_to_long(FLAG[len(FLAG)//2:])
        G1, G2 = E1.random_point(), E2.random_point()

        C1 = m1 * G1
        C2 = m2 * G2

        return (
            f"[+] G1 = {G1}\n"
            f"[+] G2 = {G2}\n"
            f"[+] C1 = {C1}\n"
            f"[+] C2 = {C2}\n"
        )

    def handle_client(conn):
        try:
            conn.sendall(b"[+] Welcome to eccOS!\n")
            conn.sendall(b"[1] Set your curve parameters\n[2] Get your curve parameters\n[3] Exit\n")

            check = False
            p, a, b, q = None, None, None, None

            while True:
                conn.sendall(b"[>] ")
                opt = conn.recv(1024).decode().strip()
                if opt == "1":
                    conn.sendall(b"[+] Enter prime p: ")
                    p = int(conn.recv(1024).decode().strip())
                    if not isPrime(p) or p.bit_length() < 128:
                        conn.sendall(b"[-] Invalid prime.\n")
                        return
                    q = 2*p+1 if isPrime(2*p+1) else conn.sendall(b"[-] Try again.")
                    conn.sendall(b"[+] Enter curve parameter a: ")
                    a = int(conn.recv(1024).decode().strip())
                    conn.sendall(b"[+] Enter curve parameter b: ")
                    b = int(conn.recv(1024).decode().strip())
                    check = True
                elif opt == "2":
                    if not check:
                        conn.sendall(b"[-] Please send your parameters first!!\n")
                    else:
                        out = send_points(p, a, b, q)
                        conn.sendall(out.encode())
                elif opt == "3":
                    conn.sendall(b"[-] Goodbye.\n")
                    return
                else:
                    conn.sendall(b"[-] Invalid option.\n")
        except Exception as e:
            conn.sendall(f"[-] Error occurred: {str(e)}\n".encode())
        finally:
            conn.close()

    def start_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(5)
            print(f"[+] Server running on {HOST}:{PORT}")
            while True:
                conn, _ = s.accept()
                multiprocessing.Process(target=handle_client, args=(conn,), daemon=True).start()

    if __name__ == "__main__":
        start_server()
