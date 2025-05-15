#!/usr/bin/env python

"""keys_manager.py: Generates a pair of RSA keys (private and public) for secure communication."""

from Crypto.PublicKey import RSA


def generate_keys(key_size: int = 2048) -> tuple[bytes, bytes]:
    """Create a new pair of RSA keys.

    Args:
        key_size (int, optional): The bit length of the desired RSA keys.
            Larger sizes offer greater security but slower performance. Defaults to 2048.

    Returns:
        tuple[bytes, bytes]:
            - private_key (bytes): The newly generated private key in DER format.
            - public_key (bytes): The corresponding public key in DER format.
    """
    # Generate a new RSA key pair with the specified key size
    key = RSA.generate(key_size)

    # Export the private key
    private_key = key.export_key()

    # Get the public key object associated with the newly created key
    public_key = key.publickey().export_key()

    return private_key, public_key
