import socket
import os
import threading

# Configuration du serveur
HOST = "0.0.0.0"
PORT = 12345
STORAGE_DIR = "server_files/"

# Creation du dossier de stockage si necessaire
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def receive_file(client_socket, filename):
    """ Reception d'un fichier envoye par le client """
    with open(os.path.join(STORAGE_DIR, filename), "wb") as f:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            f.write(data)
    
    client_socket.send(b"Fichier recu avec succes.\n")
    client_socket.shutdown(socket.SHUT_WR)  # Forcer l'envoi de la confirmation

def send_file(client_socket, filename):
    """ Envoi d'un fichier demande par le client """
    filepath = os.path.join(STORAGE_DIR, filename)
    if not os.path.exists(filepath):
        client_socket.send(b"ERREUR: Fichier introuvable.\n")
        return

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            client_socket.send(chunk)
    client_socket.send(b"EOF")  # Marquer la fin de l'envoi

def list_files(client_socket):
    """ Liste les fichiers disponibles sur le serveur """
    files = os.listdir(STORAGE_DIR)
    response = "\n".join(files).encode() if files else b"Aucun fichier disponible.\n"
    client_socket.send(response)

def delete_file(client_socket, filename):
    """ Supprime un fichier du serveur """
    filepath = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        client_socket.send(b"Fichier supprime avec succes.\n")
    else:
        client_socket.send(b"ERREUR: Fichier introuvable.\n")

def handle_client(client_socket):
    """ Gere un client avec une connexion persistante """
    print("Client connecte.")
    
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request or request.upper() == "EXIT":
                print("Client a quitte la session.")
                break

            parts = request.split(" ", 1)
            command = parts[0]
            filename = parts[1] if len(parts) > 1 else None

            if command == "UPLOAD" and filename:
                receive_file(client_socket, filename)
            elif command == "DOWNLOAD" and filename:
                send_file(client_socket, filename)
            elif command == "LIST":
                list_files(client_socket)
            elif command == "DELETE" and filename:
                delete_file(client_socket, filename)
            else:
                client_socket.send(b"Commande inconnue!\n")
        except Exception as e:
            print(f"Erreur: {e}")
            break

    client_socket.close()
    print("Connexion client fermee.")

def start_server():
    """ Demarre le serveur """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serveur FTAM en ecoute sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion acceptee de {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
