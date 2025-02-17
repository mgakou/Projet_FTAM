import socket
import os

# Configuration du client
SERVER_IP = "127.0.0.1"  # Changer si nécessaire
PORT = 5000

def send_file(filename):
    """ Envoie un fichier au serveur """
    if not os.path.exists(filename):
        print("ERREUR: Fichier non trouvé.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, PORT))
        client.send(f"UPLOAD {filename}".encode())

        with open(filename, "rb") as f:
            while chunk := f.read(4096):
                client.send(chunk)

        response = client.recv(1024).decode()
        print(f"Réponse du serveur: {response}")

def receive_file(filename):
    """ Télécharge un fichier depuis le serveur """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, PORT))
        client.send(f"DOWNLOAD {filename}".encode())

        with open(f"client_{filename}", "wb") as f:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                f.write(data)

        print(f"Fichier reçu : client_{filename}")

def main():
    """ Interface utilisateur simple """
    while True:
        print("\nOptions :")
        print("1 - Envoyer un fichier")
        print("2 - Télécharger un fichier")
        print("3 - Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            filename = input("Entrez le nom du fichier à envoyer : ")
            send_file(filename)
        elif choice == "2":
            filename = input("Entrez le nom du fichier à télécharger : ")
            receive_file(filename)
        elif choice == "3":
            print("Fermeture du client.")
            break
        else:
            print("Option invalide, réessayez.")

if __name__ == "__main__":
    main()