import socket
import pyaudio
import threading

def receive_audio(client_socket, stream):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"erro: {e}")

def send_audio(client_socket, stream):
    try:
        while True:
            data = stream.read(1024)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Error: {e}")

def start_client(ipserver):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((f'{ipserver}', 12345))

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)

    receive_thread = threading.Thread(target=receive_audio, args=(client_socket, stream))
    send_thread = threading.Thread(target=send_audio, args=(client_socket, stream))

    receive_thread.start()
    send_thread.start()

    try:
        receive_thread.join()
        send_thread.join()
    except KeyboardInterrupt:
        print("Berhenti.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

if __name__ == "__main__":
    start_client(input("Alamat Server : "))
