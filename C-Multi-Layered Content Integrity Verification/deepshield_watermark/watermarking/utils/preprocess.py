#!/usr/bin/env python

"""preprocess.py: Preprocessing utilities for any image."""

import random
from typing import Literal, Optional

import numpy as np
import torch
from PIL import Image, ImageFile
from torchvision import transforms


def normalize_array(arr, scale=255, dtype=np.uint8) -> np.ndarray:
    """Normalize an array so that its values range from 0 to the specified scale,
    then converts it to the desired data type.

    This function first shifts the minimum value in the array to zero, scales all
    elements such that the maximum element becomes equal to 'scale', and finally
    casts the entire array to the provided data type.

    Args:
        arr (np.ndarray): The input NumPy array to be normalized.
        scale (int, optional): The scaling factor which defines the upper bound of the normalization
            range. Default is set to 255, typical for image processing applications where pixel
            intensity ranges from 0-255.
        dtype (np.dtype, optional): The target data type after conversion. Common choices include
            np.uint8 or float types. Default is np.uint8.

    Returns:
        np.ndarray: A new NumPy array containing the scaled and converted values of the original
            array.
    """
    arr = arr - np.min(arr)  # Shift to start at 0
    arr = (arr / np.max(arr)) * scale  # Scale
    return arr.astype(dtype)
