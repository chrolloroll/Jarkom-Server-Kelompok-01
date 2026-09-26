import random
import time

from common.protocol import Service, Verdict, Event, build_notify
from common.matrix_ops import determinant_3x3, inverse_3x3

MATRIX_SERVICES = (Service.MATRIX_OPS,)


class MatrixServiceMixin:
    def compute_matrix(self, payload):
        m = payload["matrix"]
        det = determinant_3x3(m)
        inv = inverse_3x3(m)
        return {"determinant": det, "inverse": inv, "invertible": inv is not None}

    def corrupt_matrix(self, correct_result):
        corrupted = dict(correct_result)
        corrupted["determinant"] = correct_result["determinant"] + random.choice([-5, -1, 1, 5, 10])
        return corrupted


class AckMixin:
    def _handle_ack(self, msg):
        service = msg["service"]
        verdict = msg["verdict"]
        msg_id = msg["id"]

        self.log(f"ACK diterima id={msg_id} service={service} verdict={verdict}")

        if verdict != Verdict.INCORRECT:
            return

        with self.lock:
            already_disabled = not self.service_enabled.get(service, False)
            if not already_disabled:
                self.service_enabled[service] = False
            remaining = [s for s, v in self.service_enabled.items() if v]

        if already_disabled:
            return

        self.log(f">>> Layanan {service} DINONAKTIFKAN karena client melaporkan jawaban salah")
        self.broadcast(build_notify(
            Event.SERVICE_DISABLED,
            f"Layanan {service} dinonaktifkan karena mengirim jawaban salah.",
            service=service,
        ))

        if not remaining:
            self.log(">>> Semua layanan sudah nonaktif. Server akan berhenti.")
            self.broadcast(build_notify(
                Event.SERVER_SHUTDOWN,
                "Semua layanan telah dinonaktifkan. Server menghentikan proses.",
            ))
            self.shutdown_event.set()
            time.sleep(0.5)  
            self.stop()
