#!/usr/bin/env python

"""sha256.py: Generating Watermarking using SHA256."""

from typing import Tuple

import numpy as np
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from watermarking.generator.base import IWatermarkGenerator


class SHA256WatermarkGenerator(IWatermarkGenerator):
    """Use SHA256 hashing + RSA signature to produce a unique signature."""

    def sign(self, image: np.ndarray, private_key: bytes) -> Tuple[bytes, SHA256.SHA256Hash]:
        """Generate a signature with hashing.

        Args:
            image (np.ndarray): Source image data.
                Shape: Arbitrary (e.g., height, width, channels)
                Dtype: uint8 (assumed for tobytes() compatibility)
            private_key (bytes): RSA private key for digital signatures.

        Returns:
            bytes: The signature of the hashed image with the private key
            SHA256Hash: The hashed image using SHA256
        """
        # Convert image to raw bytes for hashing
        matrix_bytes = image.tobytes()

        # Initialize SHA256 hash object with image bytes
        hash_obj = SHA256.new(matrix_bytes)

        # Load private RSA key from provided bytes for digital signing
        private_key_rsa = RSA.import_key(private_key)

        # Sign the hash object using PKCS#1 v1.5 padding for security
        signature = pkcs1_15.new(private_key_rsa).sign(hash_obj)

        return signature, hash_obj

    def generate(self, image: np.ndarray, private_key: bytes, watermark_length: int) -> np.ndarray:
        """Generate a binary watermark array through cryptographic hashing and signing.

        Args:
            image (np.ndarray): Source image data.
                Shape: Arbitrary (e.g., height, width, channels)
                Dtype: uint8 (assumed for tobytes() compatibility)
            private_key (bytes): RSA private key for digital signatures.
            watermark_length (int): Number of bits desired in the output watermark.

        Returns:
            np.ndarray: Binary watermark array consisting of +1/-1 values.
                Shape: (watermark_length,)
                Dtype: int (for representing +1/-1 binary equivalents)
        """
        signature, _ = self.sign(image, private_key)

        # Convert signature to binary string representation
        binary_representation = "".join(format(byte, "08b") for byte in signature)

        # Trim binary string to requested watermark length & convert to +/-1 array
        watermark_array = np.array(
            [1 if bit == "1" else -1 for bit in binary_representation[:watermark_length]], dtype=int
        )

        return watermark_array

    def verify_signature(self, image: np.ndarray, private_key: bytes, public_key: bytes) -> bool:
        """Verify the signature of the image with the public key.

        Args:
            image (np.ndarray): Source image data.
                Shape: Arbitrary (e.g., height, width, channels)
                Dtype: uint8 (assumed for tobytes() compatibility)
            private_key (bytes): RSA private key for digital signatures.
            public_key (bytes): RSA public key for digital signatures.

        Returns:
            bool: The result of the signature of the image using the public key
        """
        signature, image_hash = self.sign(image, private_key)

        public_key_rsa = RSA.import_key(public_key)
        try:
            pkcs1_15.new(public_key_rsa).verify(image_hash, signature)
            return True
        except (ValueError, TypeError):
            return False
