"""
Kumpulan fungsi pengolahan string. Dipakai bersama oleh Server (untuk
menghitung jawaban) dan Client (untuk memverifikasi jawaban server
secara independen).
"""

VOWELS = set("aiueoAIUEO")


def count_characters(text: str) -> int:
    """Jumlah karakter (termasuk spasi & tanda baca) dalam string."""
    return len(text)


def count_words(text: str) -> int:
    """Jumlah kata, dipisahkan oleh satu atau lebih whitespace."""
    return len(text.split())


def reverse_string(text: str) -> str:
    """String dengan urutan karakter dibalik."""
    return text[::-1]


def remove_vowels(text: str) -> str:
    """String tanpa huruf vokal (a, i, u, e, o - besar maupun kecil)."""
    return "".join(ch for ch in text if ch not in VOWELS)
