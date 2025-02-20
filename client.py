import socket
import os

# Configuration du client
SERVER_IP = "127.0.0.1"  # Adresse IP du serveur
PORT = 12345  # Port du serveur

def send_file(client, filename):
    """ Envoie un fichier au serveur """
    if not os.path.exists(filename):
        print("ERREUR: Fichier non trouvé.")
        return

    client.send(f"UPLOAD {filename}".encode())  # Envoyer la commande au serveur
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            client.send(chunk)

    client.send(b"EOF")  # Indiquer la fin du transfert
    response = client.recv(1024).decode()  # Lire la confirmation du serveur
    print(f"Réponse du serveur: {response}")

    # Forcer une pause avant d'envoyer une nouvelle commande
    import time
    time.sleep(0.5)  # Petite pause pour éviter la fermeture prématurée

def receive_file(client, filename):
    """ Télécharge un fichier depuis le serveur """
    client.send(f"DOWNLOAD {filename}".encode())  # Envoyer la commande au serveur

    with open(filename, "wb") as f:
        while True:
            data = client.recv(4096)
            if data.endswith(b"EOF"):  # Vérifier la fin du fichier
                f.write(data[:-3])  # Enlever "EOF" avant d'écrire
                break
            f.write(data)

    print(f"Fichier téléchargé : {filename}")

def list_files(client):
    """ Demande la liste des fichiers disponibles sur le serveur """
    client.send("LIST".encode())
    response = client.recv(4096).decode()
    print("Fichiers disponibles:\n" + response)
def delete_file(client, filename):
    """ Demande la suppression d'un fichier sur le serveur """
    client.send(f"DELETE {filename}".encode())  # Envoyer la commande au serveur
    response = client.recv(1024).decode()  # Attendre la confirmation
    print(f"Réponse du serveur: {response}")  # Afficher la réponse du serveur

def show_menu():
    """ Affiche le menu des options """
    print("\n--- MENU FTAM ---")
    print("1 - Envoyer un fichier")
    print("2 - Telecharger un fichier")
    print("3 - Lister les fichiers")
    print("4 - Supprimer un fichier")
    print("5 - Quitter")
    choice = input("Choisissez une option : ")
    return choice

def main():
    """ Connexion persistante et gestion du menu """
    print("Connexion au serveur...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    print("Connexion etablie avec le serveur.")

    while True:
        choice = show_menu()

        if choice == "1":
            filename = input("Entrez le nom du fichier a envoyer : ")
            send_file(client, filename)
        elif choice == "2":
            filename = input("Entrez le nom du fichier a telecharger : ")
            receive_file(client, filename)
        elif choice == "3":
            list_files(client)
        elif choice == "4":
            filename = input("Entrez le nom du fichier a supprimer : ")
            delete_file(client, filename)
        elif choice == "5":
            client.send("EXIT".encode())  # Informer le serveur avant de quitter
            print("Deconnexion du serveur...")
            break
        else:
            print("Option invalide, reessayez.")

    client.close()
    print("Connexion fermee.")

if __name__ == "__main__":
    main()
