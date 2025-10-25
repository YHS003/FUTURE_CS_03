# crypto.py - AES-128 CBC helper functions
# -------------------------------------------------------------
# This module provides two main helper functions:
# - encrypt_bytes(): Encrypts plaintext bytes using AES-128-CBC
# - decrypt_bytes(): Decrypts ciphertext bytes back to plaintext
#
# Uses PyCryptodome library.
# -------------------------------------------------------------

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# -------------------------------------------------------------
# AES Encryption
# -------------------------------------------------------------
def encrypt_bytes(key: bytes, plaintext: bytes) -> bytes:
    """
    Encrypts a byte string using AES-128 in CBC mode.

    Parameters:
        key (bytes): AES encryption key (16 bytes for AES-128)
        plaintext (bytes): The data to be encrypted

    Returns:
        bytes: Concatenation of IV (16 bytes) + ciphertext
    """

    # Generate a random 16-byte initialization vector (IV)
    iv = os.urandom(16)

    # Create AES cipher in CBC mode with the generated IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Encrypt data (pad to make it a multiple of AES block size = 16 bytes)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))

    # Return IV concatenated with ciphertext (IV is needed for decryption)
    return iv + ct

# -------------------------------------------------------------
# AES Decryption
# -------------------------------------------------------------
def decrypt_bytes(key: bytes, blob: bytes) -> bytes:
    """
    Decrypts a byte string previously encrypted by encrypt_bytes().

    Parameters:
        key (bytes): AES decryption key (same as encryption key)
        blob (bytes): The encrypted data (IV + ciphertext)

    Returns:
        bytes: Decrypted plaintext
    """

    # Ensure blob has at least 16 bytes (IV)
    if len(blob) < 16:
        raise ValueError("Encrypted blob too short")

    # Extract the first 16 bytes as IV, the rest as ciphertext
    iv = blob[:16]
    ct = blob[16:]

    # Create AES cipher in CBC mode with the same IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Decrypt and unpad to retrieve the original plaintext
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return pt
