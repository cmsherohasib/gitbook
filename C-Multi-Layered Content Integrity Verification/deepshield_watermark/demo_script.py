# %% [markdown]
## Step 1: Register an Image


# %%
from demo.demo_utils import load_image

# Load the original image from the specified path
original_image_path = "demo/data/1_original.jpg"
original_image = load_image(original_image_path)


# %%
from demo.demo_utils import watermark_image

# Apply watermark to the original image and get the watermarked image and ground truth watermark
watermarked_img, ground_truth_watermark = watermark_image(original_image)
watermarked_img


# %%
from demo.secublox import register_image

# Register the watermarked image with the ground truth watermark using the secublox endpoint
result = register_image(watermarked_img, ground_truth_watermark)  # secublox endpoint call
result


# %% [markdown]
## Step 2: Verify an Image


# %%
from demo.demo_utils import image_verify, semantic_integrity
from demo.secublox import retrieve_wm_images
import numpy as np

def verify(candidate_image: np.ndarray) -> list[tuple[bool, np.ndarray]]:
    """
    Verify the candidate image against watermarked images retrieved from the database.

    Args:
        candidate_image (np.ndarray): The candidate image to be verified.

    Returns:
        list[tuple[bool, np.ndarray]]: A list of tuples containing a boolean indicating if the image is valid
        and the matched image.
    """
    # Retrieve watermarked images from the database
    images = retrieve_wm_images()

    # List to store images that match the candidate image
    matches = []
    for image in images:
        gt_watermark = image["watermark_matrix"]
        is_match = image_verify(candidate_image, gt_watermark)
        if is_match:
            matches.append(image)

    # List to store the verification results
    results = []
    for matched_image in matches:
        # Check the semantic integrity of the matched image with the candidate image
        is_valid, _ = semantic_integrity(matched_image, candidate_image)
        results.append((is_valid, matched_image))

    return results


# %% [markdown]
## Persona: user who wants to verify an image


# %%
from demo.demo_utils import load_image
from PIL import Image

# Load the candidate image from the specified path
candidate_image_path = "demo/data/1_watermarked.jpg"
candidate_image = load_image(candidate_image_path)

# Display the candidate image
Image.fromarray(candidate_image)


# %%
# Verify the candidate image
results = verify(candidate_image)
results

