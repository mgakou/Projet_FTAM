import socket
import os

# Configuration du serveur
HOST = "0.0.0.0"
PORT = 5000
STORAGE_DIR = "server_files/"

# Vérification et création du dossier de stockage si nécessaire
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        command, filename = request.split(" ", 1)

        if command == "UPLOAD":
            receive_file(client_socket, filename)
            client_socket.send(b"Fichier recu avec succes.\n")

        elif command == "DOWNLOAD":
            send_file(client_socket, filename)

        else:
            client_socket.send(b"Commande inconnue!\n")

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        client_socket.close()

def receive_file(client_socket, filename):
    """ Réception d'un fichier envoyé par le client """
    with open(os.path.join(STORAGE_DIR, filename), "wb") as f:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            f.write(data)

def send_file(client_socket, filename):
    """ Envoi d'un fichier demandé par le client """
    filepath = os.path.join(STORAGE_DIR, filename)
    if not os.path.exists(filepath):
        client_socket.send(b"ERREUR: Fichier introuvable.\n")
        return

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            client_socket.send(chunk)

def start_server():
    """ Démarrer le serveur """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serveur FTAM en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion établie avec {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()