#!/usr/bin/env python

"""base.py: Base for the Watermark Generator."""

from abc import ABC, abstractmethod

import numpy as np


class IWatermarkGenerator(ABC):
    """Interface for generating a watermark array given an image and a key."""

    @abstractmethod
    def generate(
        self,
        image: np.ndarray,  # Input image (NumPy array)
        private_key: bytes,  # Private encryption key (byte string)
        watermark_length: int,  # Desired output watermark length (integer)
    ) -> np.ndarray:  # Output watermark array (NumPy array)
        """Generate a watermark array using the provided inputs.

        Args:
            image (np.ndarray): Input image data.
                Shape: Arbitrary (e.g., height, width, channels)
                Dtype: uint8 (or compatible with implementation specifics)
            private_key (bytes): Secret key for securing the watermark generation process.
            watermark_length (int): Desired length of the generated watermark array.

        Returns:
            np.ndarray: Generated watermark data.
                Shape: (watermark_length,)
                Dtype: Implementation-specific (commonly bool, float32, etc.)

        Raises:
            NotImplementedError: Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement 'generate'.")
