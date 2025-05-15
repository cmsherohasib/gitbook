#!/usr/bin/env python

"""base.py: Base for the calculating Watermark Positions."""

from abc import ABC, abstractmethod

import numpy as np


class IWatermarkPositions(ABC):
    """Interface for generating positions within the frequency or spatial domain
    to embed the watermark bits.
    """

    @abstractmethod
    def generate_positions(self, public_key: bytes, watermark_length: int) -> np.ndarray:
        """Computes an array of positions for embedding watermark bits.

        These positions can be utilized within either the frequency or spatial
        domain, depending on the underlying implementation strategy.

        Args:
            public_key (bytes): Public identifier influencing position generation.
            watermark_length (int): Number of positions to generate, matching
                the expected number of watermark bits.

        Returns:
            np.ndarray: Positional data for watermark embedding.
                Shape: (watermark_length,) or (watermark_length, n_dims)
                    (where n_dims depends on the domain and implementation)
                Dtype: Typically int32 or int64, depending on the coordinate range

        Raises:
            NotImplementedError: Subclasses must provide their own implementation.
        """
        raise NotImplementedError("Subclasses must implement 'generate_positions'.")
