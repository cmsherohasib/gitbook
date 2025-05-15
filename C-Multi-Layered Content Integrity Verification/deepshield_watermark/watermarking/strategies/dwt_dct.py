#!/usr/bin/env python

"""dwt_dct.py: Watermarking Technique - 2DWT+DCT."""

import numpy as np

from watermarking.strategies.base import IWatermarkMethod
from watermarking.utils.preprocess import normalize_array
from watermarking.utils.watermark_encode_decode import dwt2dct_decode_2d, dwt2dct_encode_2d


class DWT2DCTWatermarkMethod(IWatermarkMethod):
    """Implementation of DWT (Discrete Wavelet Transform) + DCT (Discrete Cosine Transform)
    watermarking strategy.

    This method leverages the frequency domain characteristics of images to embed watermarks
    in a way that balances imperceptibility and robustness.
    """

    def embed(
        self,
        image: np.ndarray,
        watermark: np.ndarray,
        watermark_positions: np.ndarray,
        alpha: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate the watermarked image and return f(I) of the input image.

        Args:
            image (np.ndarray): The original host image.
            watermark (np.ndarray): The watermark sequence.
            watermark_positions (np.ndarray): Placement indices within the transformed space.
            alpha (float): Embedding strength.

        Returns:
            tuple[np.ndarray, np.ndarray]: The watermarked image and ground truth watermark matrix
                considering the watermark position.
        """
        assert len(image.shape) == 3, "Expecting 3D [H,W,C] image"
        _, _, channels = image.shape

        # Prepare output image (float to avoid rounding issues)
        watermarked_image = np.zeros_like(image, dtype=np.float64)

        ground_truth_per_channel = []

        for ch in range(channels):
            image_channel = image[:, :, ch].astype(np.float64)

            image_channel = normalize_array(image_channel, scale=1, dtype=np.float64)

            # Apply combined DWT & DCT encoding to decompose the image into frequency components
            coeffs, coeffs2, (diag_even_freq, diag_odd_freq) = dwt2dct_encode_2d(image_channel)

            # Make ground-truth array for this channel same length as diag_even_freq
            gt_ch = np.zeros_like(diag_even_freq, dtype=int)

            # Insert watermark bits at those positions
            gt_ch[watermark_positions] = watermark

            diag_even_freq_new = diag_even_freq.copy()
            diag_odd_freq_new = diag_odd_freq.copy()

            avg_val = 0.5 * (
                diag_even_freq[watermark_positions] + diag_odd_freq[watermark_positions]
            )

            # Compute new diagonal values reflecting the embedded watermark with controlled strength
            xp1 = avg_val + alpha * watermark  # Even diagonal with positive offset
            xp2 = avg_val - alpha * watermark  # Odd diagonal with negative offset
            # Update frequency coefficients with embedded watermark signals
            diag_even_freq_new[watermark_positions] = xp1
            diag_odd_freq_new[watermark_positions] = xp2

            # inverse transform
            output_channel = dwt2dct_decode_2d(
                coeffs, coeffs2, (diag_even_freq_new, diag_odd_freq_new), image_channel.shape
            )
            output_channel = normalize_array(output_channel)
            watermarked_image[:, :, ch] = output_channel

            # store ground truth + mask
            ground_truth_per_channel.append(gt_ch)

        # Convert all to np arrays
        ground_truth_watermark = np.stack(ground_truth_per_channel, axis=-1)

        return watermarked_image, ground_truth_watermark

    def extract(self, image: np.ndarray, watermark_positions: np.ndarray) -> np.ndarray:
        """Extract a previously embedded watermark from a given image.

        Args:
            image (np.ndarray): The image containing the embedded watermark.
            watermark_positions (np.ndarray): Original placement indices within the transformed
                space.

        Returns:
            np.ndarray: The extracted watermark sequence.
        """
        assert len(image.shape) == 3, f"Image needs to be 3D (H, W, C), got {image.shape}"
        channels = image.shape[2]
        watermarks_extracted = []

        for channel in range(channels):
            image_channel = image[:, :, channel]

            # Preprocess image identically to embedding step for consistency
            image_channel = normalize_array(image_channel, scale=1, dtype=np.float64)

            # Apply forward transforms up to the point of interest (frequency diagonals)
            _, _, (diag_even_freq, diag_odd_freq) = dwt2dct_encode_2d(image_channel)

            # Recover watermark by examining the difference between the two affected diagonals
            diag_extraction = (
                diag_even_freq[watermark_positions] - diag_odd_freq[watermark_positions]
            )

            # Binarize the extracted signal to match the expected discrete watermark values
            watermark_extracted = np.where(diag_extraction >= 0, 1, -1)
            watermarks_extracted.append(watermark_extracted)

        return np.mean(watermarks_extracted, axis=0)

    def extract_watermark_matrix(self, watermarked_image: np.ndarray) -> np.ndarray:
        """
        Extracts the embedded watermark from the watermarked image
        using the difference (diag_even_freq - diag_odd_freq) / (2*alpha).

        Args:
            watermarked_image (np.ndarray): The image that already contains the embedded watermark.

        Returns:
            np.ndarray: The extracted signed watermark values.
        """
        # Check shape
        _, _, channels = watermarked_image.shape

        # List to hold watermark parts from each channel
        extracted_parts = []

        for ch in range(channels):
            channel_data = watermarked_image[:, :, ch]

            # Decompose with the same transform (DWT -> DWT -> DCT)
            _, _, (diag_even_freq, diag_odd_freq) = dwt2dct_encode_2d(channel_data)

            # Recover the watermark values
            # Ideally it should be w = diff / (2 * alpha)
            # To make HE computation easier, w = diff
            w_channel = diag_even_freq - diag_odd_freq

            extracted_parts.append(w_channel)

        # Concatenate or flatten across channels
        extracted_watermark = np.stack(extracted_parts, axis=-1)

        # Round to nearest integer to get exact +/-1:
        extracted_watermark = np.sign(extracted_watermark).astype(int)

        return extracted_watermark

    def is_similar(
        self, extracted_watermark: np.ndarray, gt_watermark: np.ndarray, threshold: float
    ) -> tuple[bool, float]:
        """Simple watermark similarity check: percentage of matching (non-zero) positions.

        Args:
            extracted_watermark (np.ndarray): The extracted watermark as a numpy array.
            gt_watermark (np.ndarray): The ground truth watermark as a numpy array.
            threshold (float): The similarity threshold percentage.

        Returns:
            tuple[bool, float]: Tuple of similarity check and similarity score.
                - True if the similarity percentage is greater than the threshold, False otherwise.
                - Similarity score representing the similarity between extracted_watermark and gt_watermark.
        """
        if extracted_watermark.shape != gt_watermark.shape:
            return False, 0.0  # If the shapes do not match, return a similarity score of 0.0 with False. 

        # Identify non-zero positions in the ground truth watermark
        valid = gt_watermark != 0

        # Count the number of matching positions between the extracted and ground truth watermarks
        correct = np.sum(extracted_watermark[valid] == gt_watermark[valid])

        # Count the total number of non-zero positions in the ground truth watermark
        total = np.sum(valid)

        # Calculate the similarity percentage
        similarity_pct = 100.0 * correct / total if total > 0 else 0.0

        print(f"Similarity Score: {similarity_pct}")
        
        # Return True if the similarity percentage is greater than the threshold, otherwise False
        return similarity_pct > threshold, similarity_pct # We return it because we need it for the similarity score.
