import cv2
from PIL import Image

from watermarking.generator.sha256 import SHA256WatermarkGenerator
from watermarking.positions.sha256 import SHA256Positions
from watermarking.strategies.dwt_dct import DWT2DCTWatermarkMethod
from watermarking.utils.key_manager import generate_keys
from watermarking.utils.preprocess import normalize_array


def main() -> None:
    """
    Main function to demonstrate watermark embedding and extraction.
    """
    # Initialize watermark generator, positions generator, and watermarking method
    watermark_generator = SHA256WatermarkGenerator()
    watermark_positions_gen = SHA256Positions()
    watermarking_method = DWT2DCTWatermarkMethod()

    # Generate public/private key
    private_key, public_key = generate_keys()

    # Watermark length
    watermark_length = 255
    
    # Alpha (α) controls the strength of the watermark embedded in the image.
    # - A lower α value (e.g., 0.05) results in a less visible watermark, reducing potential distortion but making extraction more difficult.
    # - A higher α value (e.g., 0.2) increases the visibility of the watermark, making it easier to extract but potentially distorting the original image.
    # - The choice of α should balance invisibility and robustness, depending on the application's security and perceptual needs.
    alpha = 0.1

    # Read an image and insert the watermark inside
    original_image = cv2.imread("image.png")
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    original_image = Image.fromarray(original_image)
    original_image = original_image.convert("RGB")
    original_image = normalize_array(original_image)

    # Generate the watermark based on the image and private key
    watermark = watermark_generator.generate(
        image=original_image, private_key=private_key, watermark_length=watermark_length
    )

    # Calculate positions for embedding the watermark
    watermark_positions = watermark_positions_gen.generate_positions(
        public_key=public_key, watermark_length=watermark_length
    )

    # Embed the watermark into the image using the selected method
    watermarked_image, ground_truth_watermark = watermarking_method.embed(
        image=original_image,
        watermark=watermark,
        watermark_positions=watermark_positions,
        alpha=alpha,
    )

    # Save the watermarked image and any of the needed information
    reconstructed_image = Image.fromarray(normalize_array(watermarked_image))
    reconstructed_image.save("watermarked_image.png")

    # Load a watermarked image and verify if watermark exists or not
    candidate_image = cv2.imread("watermarked_image.png")
    candidate_image = cv2.cvtColor(candidate_image, cv2.COLOR_BGR2RGB)
    candidate_image = Image.fromarray(candidate_image)
    candidate_image = candidate_image.convert("RGB")
    candidate_image = normalize_array(candidate_image)

    extracted_watermark = watermarking_method.extract_watermark_matrix(candidate_image)

    # Verify if the watermark is valid or not
    # If the watermark is a perfect match, then the Similarity Score will be 100.
    # If the watermark is a complete inverse then the Similarity Score will be -100.
    # If the watermark is completely random, then the Similarity Score will be 0.
    is_similar, similarity_score = watermarking_method.is_similar(
        extracted_watermark=extracted_watermark,
        gt_watermark=ground_truth_watermark,
        threshold=80,
    )
    print(f"Is extracted watermark similar: {is_similar}, similarity_score: {similarity_score}")

if __name__ == "__main__":
    main()
