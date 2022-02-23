def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = []
    for i, _ in enumerate(plaintext):
        if i > len(keyword) - 1:
            symb = i % len(keyword)
            shift = (
                ord(keyword[symb]) - ord("A")
                if keyword[symb].isupper()
                else ord(keyword[symb]) - ord("a")
            )
        else:
            shift = (
                ord(keyword[i]) - ord("A") if keyword[i].isupper() else ord(keyword[i]) - ord("a")
            )

        if plaintext[i].isalpha():
            b = chr(ord(plaintext[i]) + shift)
            b = chr(ord(b) - 26) if not b.isalpha() or plaintext[i].islower() != b.islower() else b
            ciphertext.append(b)
        else:
            ciphertext.append(plaintext[i])
    return "".join([str(i) for i in ciphertext])


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = []
    for i, _ in enumerate(ciphertext):
        if i > len(keyword) - 1:
            symb = i % len(keyword)
            shift = (
                ord(keyword[symb]) - ord("A")
                if keyword[symb].isupper()
                else ord(keyword[symb]) - ord("a")
            )
        else:
            shift = (
                ord(keyword[i]) - ord("A") if keyword[i].isupper() else ord(keyword[i]) - ord("a")
            )

        if ciphertext[i].isalpha():
            b = chr(ord(ciphertext[i]) - shift)
            b = chr(ord(b) + 26) if not b.isalpha() or ciphertext[i].islower() != b.islower() else b
            plaintext.append(b)
        else:
            plaintext.append(ciphertext[i])
    return "".join([str(i) for i in plaintext])
