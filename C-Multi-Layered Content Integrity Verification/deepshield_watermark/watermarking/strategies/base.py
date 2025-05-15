#!/usr/bin/env python

"""base.py: Base for the all Watermarking Technique."""

from abc import ABC, abstractmethod

import numpy as np


class IWatermarkMethod(ABC):
    """
    Defines the interface for any watermarking method
    (embed and extract).
    """

    @abstractmethod
    def embed(
        self,
        image: np.ndarray,
        watermark: np.ndarray,
        watermark_positions: np.ndarray,
        alpha: float,
    ) -> np.ndarray:
        """Embed `watermark` into `image` at `watermark_positions` with intensity `alpha`.

        Args:
            image (np.ndarray): The host image.
            watermark (np.ndarray): Data to be hidden within the image.
            watermark_positions (np.ndarray): Coordinates specifying where to embed the watermark.
            alpha (float): Embedding strength (range: 0.0 to 1.0].

        Returns:
            np.ndarray: The watermarked image.

        Raises:
            NotImplementedError: Concrete classes must implement this method.
        """
        raise NotImplementedError("Implement 'embed' in a subclass.")

    @abstractmethod
    def extract(self, image: np.ndarray, watermark_positions: np.ndarray) -> np.ndarray:
        """Extracts the previously embedded watermark from a given `image`.

        Args:
            image (np.ndarray): Possibly distorted image containing the watermark.
            watermark_positions (np.ndarray): Original coordinates used during embedding.

        Returns:
            np.ndarray: The extracted watermark data.

        Raises:
            NotImplementedError: Subclasses are responsible for implementing this method.
        """
        raise NotImplementedError("Provide an 'extract' implementation in a derived class.")
