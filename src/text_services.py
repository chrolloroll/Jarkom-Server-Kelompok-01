import random

from common.protocol import Service
from common.text_ops import count_characters, count_words, reverse_string, remove_vowels

TEXT_SERVICES = (
    Service.COUNT_CHAR,
    Service.COUNT_WORD,
    Service.REVERSE_STRING,
    Service.REMOVE_VOWELS,
)


class TextServiceMixin:
    def compute_text(self, service, payload):
        if service == Service.COUNT_CHAR:
            return count_characters(payload["text"])
        if service == Service.COUNT_WORD:
            return count_words(payload["text"])
        if service == Service.REVERSE_STRING:
            return reverse_string(payload["text"])
        if service == Service.REMOVE_VOWELS:
            return remove_vowels(payload["text"])
        raise ValueError(f"Bukan layanan teks: {service}")

    def corrupt_text(self, service, correct_result):
        if service in (Service.COUNT_CHAR, Service.COUNT_WORD):
            return correct_result + random.choice([-2, -1, 1, 2, 3])
        if service in (Service.REVERSE_STRING, Service.REMOVE_VOWELS):
            if len(correct_result) == 0:
                return correct_result + "X"
            idx = random.randrange(len(correct_result))
            ch = random.choice("!?#@X")
            return correct_result[:idx] + ch + correct_result[idx + 1:]
        return correct_result
