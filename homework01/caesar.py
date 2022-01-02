import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = []
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            b = chr(ord(plaintext[i]) + shift % 26)
            if not b.isalpha() or plaintext[i].islower() != b.islower():
                b = chr(ord(b) - 26)
            ciphertext.append(b)
        else:
            ciphertext.append(plaintext[i])
    return "".join([str(i) for i in ciphertext])


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = []
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            b = chr(ord(ciphertext[i]) - shift % 26)
            if not b.isalpha() or ciphertext[i].islower() != b.islower():
                b = chr(ord(b) + 26)
            plaintext.append(b)
        else:
            plaintext.append(ciphertext[i])
    return "".join([str(i) for i in plaintext])


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift


if __name__ == "__main__":
    print(decrypt_caesar(encrypt_caesar("python", 14), 14))
