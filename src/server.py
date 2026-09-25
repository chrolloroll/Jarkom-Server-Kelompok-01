import argparse
import socket
import sys
import threading
import time

from common.protocol import Service

from connection_handler import ConnectionMixin
from text_services import TextServiceMixin, TEXT_SERVICES
from matrix_services import MatrixServiceMixin, AckMixin, MATRIX_SERVICES

CORRUPTION_PROBABILITY = 0.3  # peluang server mengirim jawaban salah


class Server(ConnectionMixin, TextServiceMixin, MatrixServiceMixin, AckMixin):
    def __init__(self, host="0.0.0.0", port=5000, corruption_prob=CORRUPTION_PROBABILITY):
        self.host = host
        self.port = port
        self.corruption_prob = corruption_prob

        self.service_enabled = {s: True for s in Service.ALL}
        self.lock = threading.Lock()

        self.clients = []           # list of (conn, addr) yang sedang terhubung
        self.clients_lock = threading.Lock()

        self.shutdown_event = threading.Event()
        self._sock = None

    # ----------------------------------------------------------------
    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] [SERVER] {msg}", flush=True)

    def enabled_services(self):
        with self.lock:
            return [s for s, v in self.service_enabled.items() if v]

    # ----------------------------------------------------------------
    # Dispatcher: meneruskan ke layanan teks (Person 3) atau matriks (Person 4)
    # ----------------------------------------------------------------
    def compute_correct(self, service, payload):
        if service in TEXT_SERVICES:
            return self.compute_text(service, payload)
        if service in MATRIX_SERVICES:
            return self.compute_matrix(payload)
        raise ValueError(f"Layanan tidak dikenal: {service}")

    def corrupt(self, service, correct_result):
        """Membuat jawaban SALAH (simulasi error acak sesuai poin 5 tugas)."""
        if service in TEXT_SERVICES:
            return self.corrupt_text(service, correct_result)
        if service in MATRIX_SERVICES:
            return self.corrupt_matrix(correct_result)
        return correct_result

    # ----------------------------------------------------------------
    def stop(self):
        with self.clients_lock:
            for conn, addr in self.clients:
                try:
                    conn.close()
                except OSError:
                    pass
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass

    # ----------------------------------------------------------------
    def run(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(5)
        self.log(f"Server berjalan di {self.host}:{self.port}")
        self.log(f"Layanan aktif: {', '.join(self.enabled_services())}")

        try:
            while not self.shutdown_event.is_set():
                self._sock.settimeout(1.0)
                try:
                    conn, addr = self._sock.accept()
                except socket.timeout:
                    continue
                t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                t.start()
        except OSError:
            pass
        finally:
            self.log("Server telah berhenti.")


def main():
    parser = argparse.ArgumentParser(description="Server Text & Matrix Service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--corrupt-prob", type=float, default=CORRUPTION_PROBABILITY,
                        help="Peluang (0-1) server mengirim jawaban salah")
    args = parser.parse_args()

    server = Server(host=args.host, port=args.port, corruption_prob=args.corrupt_prob)
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nDihentikan oleh pengguna.")
        sys.exit(0)


if __name__ == "__main__":
    main()
