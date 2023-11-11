import socket
import pyaudio
import threading

def handle_client(client_socket, address, suara):
    print(f"Koneksi didapat dari {address}")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if suara == 1:
                stream.write(data)
            else:
                pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Koneksi dari {address} Tertutup.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

def start_server(suara):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("Menunggu koneksi...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr,suara))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server berhenti.")

if __name__ == "__main__":
    start_server(int(input("0 untuk tidak mendengarkan log | 1 untuk mendengarkan log : ")))
