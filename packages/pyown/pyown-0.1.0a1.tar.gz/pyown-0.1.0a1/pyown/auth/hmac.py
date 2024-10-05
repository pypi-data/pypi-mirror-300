from hashlib import sha1, sha256
from hmac import HMAC, compare_digest
from secrets import token_bytes

from .enum import AuthAlgorithm

__all__ = [
    "client_hmac",
    "server_hmac",
    "compare_hmac",
    "create_key",
    "hex_to_digits",
    "digits_to_hex",
]


def client_hmac(
        server_key: str,
        client_key: str,
        password: str,
        client_identity: str = "736F70653E",
        server_identity: str = "636F70653E",
        hash_algorithm: AuthAlgorithm = AuthAlgorithm.SHA256,
) -> bytes:
    """
    Generate the HMAC authentication for the client.

    Args:
        server_key: The key sent by the server (Ra)
        client_key: The key generated by the client (Rb)
        password: The open password of the server (Kab = sha(kab))
        client_identity: string used to identify the client (A)
        server_identity: string used to identify the server (B)
        hash_algorithm: The hash function to use for the hmac calculation (can be sha1 or sha256)

    Returns:
        str: the client authentication string in bytes
    """
    if hash_algorithm == AuthAlgorithm.SHA1:
        hash_function = sha1
    elif hash_algorithm == AuthAlgorithm.SHA256:
        hash_function = sha256
    else:
        raise ValueError("Invalid hash algorithm")

    kab = hash_function(password.encode()).hexdigest()
    hmac_message = f"{server_key}{client_key}{client_identity}{server_identity}{kab}"

    hmac = HMAC(
        key=server_key.encode(),
        msg=hmac_message.encode(),
        digestmod=hash_function,
    )

    return hmac.digest()


def server_hmac(
        server_key: str,
        client_key: str,
        password: str,
        hash_algorithm: AuthAlgorithm = AuthAlgorithm.SHA256,
) -> bytes:
    """
    Generate the HMAC authentication for the server.

    Args:
        server_key: The key sent by the server (Ra)
        client_key: The key generated by the client (Rb)
        password: The open password of the server (Kab = sha(kab))
        hash_algorithm: The hash function to use for the hmac calculation (can be sha1 or sha256)

    Returns:
        str: the server confirmation string in bytes
    """
    if hash_algorithm == AuthAlgorithm.SHA1:
        hash_function = sha1
    elif hash_algorithm == AuthAlgorithm.SHA256:
        hash_function = sha256
    else:
        raise ValueError("Invalid hash algorithm")

    kab = hash_function(password.encode()).hexdigest()
    hmac_message = f"{client_key}{server_key}{kab}"

    hmac = HMAC(
        key=server_key.encode(),
        msg=hmac_message.encode(),
        digestmod=hash_function,
    )

    return hmac.digest()


def compare_hmac(
        hmac1: bytes,
        hmac2: bytes,
) -> bool:
    """
    Compare two hmacs in constant time.

    Args:
        hmac1: The first hmac
        hmac2: The second hmac

    Returns:
        bool: True if the hmacs are equal, False otherwise
    """
    return compare_digest(hmac1, hmac2)


def create_key(
        hash_algorithm: AuthAlgorithm = AuthAlgorithm.SHA256,
) -> str:
    """
    Create a random key for the hmac.

    Args:
        hash_algorithm: The hash function to use for the hmac calculation (can be sha1 or sha256)

    Returns:
        str: the key in hex format
    """
    if hash_algorithm == AuthAlgorithm.SHA1:
        hash_function = sha1
    elif hash_algorithm == AuthAlgorithm.SHA256:
        hash_function = sha256
    else:
        raise ValueError("Invalid hash algorithm")

    return hash_function(token_bytes(32)).hexdigest()


def hex_to_digits(
        hex_string: str,
) -> str:
    """
    Convert a hex string to digits.

    Args:
        hex_string: The hex string

    Returns:
        str: the digits string
    """
    out = ""
    for c in hex_string:
        value = int(c, 16)
        out += str(value // 10) + str(value % 10)
    return out


def digits_to_hex(
        digits_string: str,
) -> str:
    """
    Convert a digits string to hex.

    Args:
        digits_string: The digits string

    Returns:
        str: the hex string
    """
    out = ""
    for i in range(0, len(digits_string), 2):
        value = int(digits_string[i]) * 10 + int(digits_string[i + 1])
        out += hex(value)[2:]
    return out
