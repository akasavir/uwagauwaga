import socket
import xmlrpc.client

# Konfiguracja adresów i portów
HOST = "127.0.0.1"
PORT_SOCKET = 2221
PORT_RPC = 2223

# Połączenie z serwerem RPC
rpc_client = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT_RPC}")

def obsluga_klienta(conn):
    try:
        while True:
            # Odbieranie danych od klienta (AppFront-socket)
            data = conn.recv(2048)
            if not data:
                break
            # Konwersja bajtów na string
            message = data.decode("utf-8").strip()
            # Parsowanie komunikatu
            parts = message.split(";")
            if parts[0] == "1":  # Dopisanie abonenta
                imie, nr_tel = parts[1], parts[2]
                result = rpc_client.zapisz_abonenta(imie, nr_tel)
                response = result
            elif parts[0] == "2":  # Pobranie książki
                ksiazka = rpc_client.pobierz_ksiazke()
                response = str(ksiazka)
            else:
                response = "Nieznany kod operacji"
            # Wysyłanie odpowiedzi do klienta
            conn.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        conn.close()

def main():
    # Tworzenie serwera socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT_SOCKET))
        server.listen(5)
        print(f"Adapter nasłuchuje na porcie {PORT_SOCKET}")
        while True:
            conn, addr = server.accept()
            print(f"Połączono z: {addr}")
            obsluga_klienta(conn)

if __name__ == "__main__":
    main()
