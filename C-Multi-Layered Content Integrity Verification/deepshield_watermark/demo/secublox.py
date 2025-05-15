import json

import numpy as np
from demo.demo_utils import load_image
from PIL import Image


def register_image(watermarked_image: np.ndarray, ground_truth_watermark: np.ndarray) -> bool:
    """Register a watermarked image given the image array and its ground truth watermark.

    Args:
        watermarked_image (np.ndarray): The watermarked image as a NumPy array.
        ground_truth_watermark (np.ndarray): The ground truth watermark as a NumPy array.

    Returns:
        bool: True if the registration is successful, False otherwise.
    """
    # Placeholder implementation
    return True


# this is get_watermark_information, but for all images
def retrieve_wm_images() -> list[dict[str, np.ndarray]]:
    """Retrieve watermark information for all images.

    Returns:
        List[Dict[str, np.ndarray]]: A list of dictionaries, each containing the watermarked image
            and its ground truth watermark matrix.
    """
    # Load the watermark metadata from file
    json_file_path = "demo/data/watermarking_results.json"
    with open(json_file_path, "r", encoding="utf-8") as file_obj:
        watermark_metadata = json.load(file_obj)

     # Construct the list of dictionaries with watermarked images and their ground truth watermark matrices
    result = [
        {
            "image_path": f"demo/data/{i+1}_watermarked.jpg",
            "image": load_image(f"demo/data/{i+1}_watermarked.jpg"),
            "watermark_matrix": np.array(watermark_metadata["watermarked_images"][i]["gt_watermark_matrix"], dtype=np.float64),
        }
        for i in range(5)
    ]
    return result