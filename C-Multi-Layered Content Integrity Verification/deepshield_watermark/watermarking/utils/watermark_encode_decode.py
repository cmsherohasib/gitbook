#!/usr/bin/env python

"""watermark_encode_decode.py: Encode and Decode Watermarking"""

import numpy as np
from pywt import dwt2, idwt2
from scipy.fftpack import dct, idct

from watermarking.utils.zigzag import inverse_zigzag, zig_zag


def dwt2dct_encode_2d(
    image: np.ndarray,  # Input image for encoding
) -> tuple[np.ndarray, ...]:  # Tuple containing wavelet coefficients & frequency arrays
    """Encode a 2D image using a multi-step transform process.

    Args:
        image (np.ndarray): Input image data.
            - Shape: Arbitrary (height, width) or (height, width, channels)
            - Dtype: Numerical (uint8, float32, etc.; depends on `dwt2` compatibility)

    Returns:
        tuple[
            tuple[np.ndarray, ..., np.ndarray],  # Level 1 & 2 Wavelet Coefficients (LL, LH, HL, HH)
            tuple[np.ndarray, ..., np.ndarray],  # Second-Level Wavelet Coefficients
                (LL2, LH2, HL2, HH2)
            tuple[np.ndarray, np.ndarray]   # Diagonal Frequency Components after 1D DCT (even, odd)
        ]
    """
    # Perform initial 2D Wavelet Transform (Level 1)
    LL, (LH, HL, HH) = dwt2(data=image, wavelet="db1", mode="symmetric")

    # Further decompose the Approximation Coefficients (LL) with another 2D DWT (Level 2)
    LL2, (LH2, HL2, HH2) = dwt2(data=LL, wavelet="db1", mode="symmetric")

    # Rearrange LL2 coefficients in a zig-zag order to prepare for diagonal splitting
    zigzag_1d, _ = zig_zag(LL2)

    # Split zig-zagged sequence into even-indexed and odd-indexed diagonals
    diag_even = zigzag_1d[1::2]  # elements at odd indices
    diag_odd = zigzag_1d[0::2]  # elements at even indices

    # Apply Orthogonal 1D Discrete Cosine Transform to both diagonal sets
    diag_even_freq = dct(diag_even, norm="ortho")
    diag_odd_freq = dct(diag_odd, norm="ortho")

    # Bundle results across different transformation stages
    return (LL, LH, HL, HH), (LL2, LH2, HL2, HH2), (diag_even_freq, diag_odd_freq)


def dwt2dct_decode_2d(
    coeffs: tuple[np.ndarray, ...],  # Tuple of 4 arrays (LL, LH, HL, HH)
    coeffs2: tuple[np.ndarray, ...],  # Tuple of 4 arrays (LL2, LH2, HL2, HH2)
    diags: tuple[np.ndarray, np.ndarray],  # Even & Odd frequency diagonals
    image_shape: tuple[int, int],
) -> np.ndarray:
    """Decode watermarked coefficients via inverse transformations.

    Args:
        coeffs: First set of 2D DWT coefficients (Tuple of 4 ndarrays: LL, LH, HL, HH)
        coeffs2: Second set of 2D DWT coefficients (Tuple of 4 ndarrays: LL2, LH2, HL2, HH2)
        diags: Diagonal frequencies after DCT (Even, Odd)
        image_shape: The shape of the original image to resize in case of different shapes

    Returns:
        np.ndarray: Decoded watermarked output after IDWT
    """
    # Unpack coefficient tuples for easier access
    (LL, LH, HL, HH) = coeffs
    (LL2, LH2, HL2, HH2) = coeffs2
    (diag_even_freq, diag_odd_freq) = diags

    # Extract dimensions from second level low-pass filter output
    rows, cols = LL2.shape

    # Inverse DCT on Diagonals
    diag_even = idct(diag_even_freq, norm="ortho")  # Inverse DCT on even freqs
    diag_odd = idct(diag_odd_freq, norm="ortho")  # Inverse DCT on odd freqs

    # Reconstruct 1D Zig-Zag & Inverse Transformation
    zigzag_1d = np.zeros(rows * cols, dtype=float)  # Initialize 1D array
    zigzag_1d[1::2] = diag_even  # Interleave even frequencies
    zigzag_1d[0::2] = diag_odd  # Interleave odd frequencies

    # Inverse zigzag
    LL2_watermarked = inverse_zigzag(zigzag_1d, rows, cols)  # Convert back to 2D
    if LL2_watermarked.shape != LL2.shape:
        LL2_watermarked = LL2_watermarked[: LL2.shape[0], : LL2.shape[1]]

    # Two-Stage Inverse 2D Wavelet Transform
    LL_watermarked = idwt2((LL2_watermarked, (LH2, HL2, HH2)), wavelet="db1", mode="symmetric")
    if LL_watermarked.shape != LL.shape:
        LL_watermarked = LL_watermarked[: LL.shape[0], : LL.shape[1]]

    output_watermarked = idwt2((LL_watermarked, (LH, HL, HH)), wavelet="db1", mode="symmetric")
    if output_watermarked.shape != image_shape:
        output_watermarked = output_watermarked[: image_shape[0], : image_shape[1]]

    return output_watermarked
