#!/usr/bin/env python

"""sha256.py: Calculating Watermarking positions using SHA256."""

import numpy as np
from Crypto.Hash import SHA256

from watermarking.positions.base import IWatermarkPositions


class SHA256Positions(IWatermarkPositions):
    """Generate watermark positions via SHA256-based shuffling.

    Based on a provided public key, this class creates a deterministic yet unpredictable
    set of indices suitable for placing watermarks within a larger dataset.
    """

    def generate_positions(
        self,
        public_key: bytes,  # Public key used as input for SHA256 hashing
        watermark_length: int,  # Desired number of watermark positions to generate
    ) -> np.ndarray:  # Sequence of indices for watermark insertion
        """Produces a shuffled range of indices seeded by a SHA256 hash of the public key.

        The resulting positions are deterministic but practically unpredictable without knowing
        the original public key, making them suitable for covert watermarking applications.

        Args:
            public_key (bytes): Input for SHA256 hash, influencing the randomness seed.
            watermark_length (int): Number of positions to generate (minimum starting index is 2).

        Returns:
            np.ndarray: One-dimensional array containing shuffled position indices.
                - Starting point: always greater than 1 (starts at index 2)
                - Length: equals `watermark_length`
                - Dtype: integer type (dependent on platform, typically int64)
        """
        # Create a new SHA256 hash object initialized with the public key
        hash_obj = SHA256.new(public_key)

        # Derive a 32-bit seed from the digest to initialize the RNG
        seed = int.from_bytes(hash_obj.digest(), "big") % (2**32)

        # Generate initial sequential positions (start at 2, end at watermark_length + 1)
        watermark_positions = np.arange(2, watermark_length + 2)

        # Temporarily alter the global RNG state to isolate this shuffle operation
        state = np.random.get_state()  # Save current state
        np.random.seed(seed)  # Set seed derived from public key
        np.random.shuffle(watermark_positions)  # Perform shuffle
        np.random.set_state(state)  # Restore previous RNG state

        return watermark_positions
