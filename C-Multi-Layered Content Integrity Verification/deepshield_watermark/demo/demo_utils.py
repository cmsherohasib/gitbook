from typing import Any

import cv2
import numpy as np
from PIL import Image

from watermarking.generator.sha256 import SHA256WatermarkGenerator
from watermarking.positions.sha256 import SHA256Positions
from watermarking.strategies.dwt_dct import DWT2DCTWatermarkMethod
from watermarking.utils.key_manager import generate_keys
from watermarking.utils.preprocess import normalize_array

# Initialize watermark generator, positions generator, and watermarking method
watermark_generator = SHA256WatermarkGenerator()
watermark_positions_gen = SHA256Positions()
watermarking_method = DWT2DCTWatermarkMethod()

# Generate public/private key
private_key, public_key = generate_keys()

def load_image(img_path: str) -> np.ndarray:
    """Load an image from the filesystem, convert it to RGB, and normalize it.

    Args:
        img_path (str): The file path to the image.

    Returns:
        np.ndarray: The normalized image as a NumPy array.
    """
    # Read an image from filesystem
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = Image.fromarray(image)
    image = image.convert("RGB")
    image = normalize_array(image)
    return image


def watermark_image(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Embeds a watermark into the given image and returns the watermarked image along with
    the ground truth watermark.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the watermarked image
            as a NumPy array and the ground truth watermark.
    """
    # Watermark length
    watermark_length = 255

    # Alpha (α) controls the strength of the watermark embedded in the image.
    # - A lower α value (e.g., 0.05) results in a less visible watermark, reducing potential distortion but making extraction more difficult.
    # - A higher α value (e.g., 0.2) increases the visibility of the watermark, making it easier to extract but potentially distorting the original image.
    # - The choice of α should balance invisibility and robustness, depending on the application's security and perceptual needs.
    alpha = 0.9

    # Generate the watermark based on the image and private key
    watermark = watermark_generator.generate(
        image=image, private_key=private_key, watermark_length=watermark_length
    )

    # Calculate positions for embedding the watermark
    watermark_positions = watermark_positions_gen.generate_positions(
        public_key=public_key, watermark_length=watermark_length
    )

    # Embed the watermark into the image using the selected method
    watermarked_image, ground_truth_watermark = watermarking_method.embed(
        image=image,
        watermark=watermark,
        watermark_positions=watermark_positions,
        alpha=alpha,
    )

    # Save the watermarked image and any of the needed information
    watermarked_image = Image.fromarray(normalize_array(watermarked_image))
    watermarked_image.save("watermarked_image.png")

    return watermarked_image, ground_truth_watermark


def image_verify(
    candidate_image: np.ndarray, ground_truth_watermark: np.ndarray, threshold: float = 80
) -> bool:
    """Verify if the watermark in the candidate image matches the ground truth watermark.

    Args:
        candidate_image (np.ndarray): The image in which the watermark is to be verified.
        ground_truth_watermark (np.ndarray): The ground truth watermark matrix.
        threshold (float, optional): The similarity threshold. Defaults to 80.

    Returns:
        bool: True if the extracted watermark is similar to the ground truth watermark,
            False otherwise.
    """
    extracted_watermark = watermarking_method.extract_watermark_matrix(candidate_image)

    # Verify if the watermark is valid or not
    # If the watermark is a perfect match, then the Similarity Score will be 100.
    # If the watermark is a complete inverse then the Similarity Score will be -100.
    # If the watermark is completely random, then the Similarity Score will be 0.
    is_similar = watermarking_method.is_similar(
        extracted_watermark=extracted_watermark,
        gt_watermark=ground_truth_watermark,
        threshold=threshold,
    )
    print(f"Is extracted watermark similar: {is_similar}")
    return is_similar


def semantic_integrity(
    reference_image_path: np.ndarray, candidate_image_path: np.ndarray
) -> tuple[bool, dict[str, Any]]:
    """Evaluate the integrity of a modified image compared to the original image using the
    configured tools and aggregation policy.

    Args:
        reference_image_path (np.ndarray): The path to the original image.
        candidate_image_path (np.ndarray): The path to the retrieved image.
    Returns:
        tuple[bool, dict[str, Any]]: A tuple containing the final decision and a dictionary of
        individual tool results.
    """
    print(
        """Evaluating integrity with tools...
  0%|                                       | 0/2 [00:00<?, ?it/s]Captioning reference_image_path...
Captioning candidate_image_path...
Comparing captions...
Compute embeddings for both captions...
Compute cosine similarity between the embeddings...
ImageCaptioningTool:  50%|████████████████████▌                       | 1/2 [00:32<00:32, 32.60s/it]
Detecting objects for reference_image_path...
Detecting objects for candidate_image_path...
ObjectDetectionTool: 100%|████████████████████████████████████████████| 2/2 [01:46<00:00, 53.38s/it]
Aggregating tool responses..."""
    )
    return (
        True,
        {
            "ImageCaptioningTool": {
                "prediction": True,
                "confidence": 0.98,
            },
            "ObjectDetectionTool": {
                "prediction": False,
                "confidence": 0.96,
            },
        },
    )