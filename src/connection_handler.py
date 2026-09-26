import random
from common.protocol import (
    MessageReader, Status, Event, MessageType,
    build_response, build_notify, send_message,
)


class ConnectionMixin:
    def broadcast(self, message):
        """Mengirim satu pesan (mis. NOTIFY) ke semua client yang terhubung."""
        with self.clients_lock:
            targets = list(self.clients)
        for conn, addr in targets:
            try:
                send_message(conn, message)
            except OSError:
                pass

    def handle_client(self, conn, addr):
        self.log(f"Client terhubung dari {addr}")
        reader = MessageReader(conn)

        with self.clients_lock:
            self.clients.append((conn, addr))

        try:
            welcome = build_notify(
                Event.WELCOME,
                "Selamat datang. Layanan aktif: " + ", ".join(self.enabled_services()),
            )
            send_message(conn, welcome)

            while not self.shutdown_event.is_set():
                msg = reader.read_message()
                if msg is None:
                    self.log(f"Client {addr} memutus koneksi")
                    break

                if msg["type"] == MessageType.REQUEST:
                    self._handle_request(conn, addr, msg)
                elif msg["type"] == MessageType.ACK:
                    self._handle_ack(msg)
                else:
                    self.log(f"Pesan tidak dikenal dari {addr}: {msg}")
        except (ConnectionResetError, BrokenPipeError, OSError):
            self.log(f"Koneksi dengan {addr} terputus")
        finally:
            with self.clients_lock:
                if (conn, addr) in self.clients:
                    self.clients.remove((conn, addr))
            conn.close()

    def _handle_request(self, conn, addr, msg):
        service = msg["service"]
        msg_id = msg["id"]
        payload = msg.get("payload", {})

        with self.lock:
            enabled = self.service_enabled.get(service, False)

        if not enabled:
            resp = build_response(
                msg_id, service, Status.SERVICE_DISABLED,
                result=None, note=f"Layanan {service} sudah dinonaktifkan.",
            )
            send_message(conn, resp)
            self.log(f"[{addr}] REQUEST {service} id={msg_id} ditolak (layanan nonaktif)")
            return

        try:
            correct = self.compute_correct(service, payload)
        except Exception as e:
            resp = build_response(msg_id, service, Status.ERROR, result=None, note=str(e))
            send_message(conn, resp)
            return

        send_wrong = random.random() < self.corruption_prob
        result_to_send = self.corrupt(service, correct) if send_wrong else correct

        resp = build_response(msg_id, service, Status.OK, result=result_to_send)
        send_message(conn, resp)

        tag = "SALAH (sengaja)" if send_wrong else "benar"
        self.log(f"[{addr}] REQUEST {service} id={msg_id} -> jawaban {tag}: {result_to_send}")
