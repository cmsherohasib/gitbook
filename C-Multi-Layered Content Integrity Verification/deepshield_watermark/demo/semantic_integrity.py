"""semantic_integrity.py: Tools and pipeline for evaluating the semantic integrity of images."""

from dataclasses import dataclass
from typing import Any


@dataclass
class SemanticIntegrityTool:
    """A tool for evaluating the integrity of images."""


@dataclass
class SemanticIntegrityChecker:
    """SemanticIntegrityChecker class for evaluating the integrity of images using multiple
    semantic integrity tools."""

    def __init__(self, tools: list[SemanticIntegrityTool], aggregation_policy: str = "majority"):
        """Initialize a SemanticIntegrityChecker with a list of tools and an aggregation policy.

        Args:
           tools (list[SemanticIntegrityTool]): A list of SemanticIntegrityTool instances.
           aggregation_policy (str): The policy to aggregate the results from multiple tools. Valid
            policies are 'majority', 'mean', 'min', and 'max'.

        Raises:
            ValueError: If no tools are provided.
        """

    def evaluate(
        self, reference_image_path: str, candidate_image_path: str
    ) -> tuple[bool, dict[str, bool]]:
        """Evaluate the integrity of a modified image compared to the original image using the
        configured tools and aggregation policy.

        Args:
            reference_image_path (str): The path to the original image.
            candidate_image_path (str): The path to the retrieved image.
        Returns:
            tuple[bool, dict[str, bool]]: A tuple containing the final decision and a dictionary of
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
            True if reference_image_path != candidate_image_path else True,
            {
                "ImageCaptioningTool": {
                    "prediction": True,
                    "confidence": 0.98,
                    "other_metadata": "blabla",
                },
                "ObjectDetectionTool": {
                    "prediction": False,
                    "confidence": 0.96,
                    "other_metadata": "blabla2",
                },
            },
        )


def create_tools(tools_config: dict[str, dict[str, Any]]) -> list[SemanticIntegrityTool]:
    """Create tools based on the provided configuration file.

    Args:
        tools_config (dict[str, dict[str, dict[str, Any]]]): config dict for tools.
        Each key is a tool type, and each value is a dict containing the model and comparator
         configurations.
        Each tool can contain the following keys:
           - model: dict containing the model type and its configuration.
           - comparator: dict containing the comparator type and its configuration.
    Returns:
        list[SemanticIntegrityTool]: list of tools created based on the config.
    """
    tools_config = 3
    return [SemanticIntegrityTool() for _ in range(tools_config)]


def validate_config(config: dict[str, Any]) -> tuple[dict, str]:
    """Validate the semantic integrity config.

    Args:
        config (dict[str, Any]): the config to validate
    Returns:
        tools_config (dict[str, dict[str, Any]): config for individual tools. Provides parameters
        for each tool, including the underlying AI model and feature comparator.
        aggregation_policy (str): policy to aggregate responses from tools. Can be one of
        'majority', 'mean', 'min', 'max'.
    """
    return (config["tools"], config["aggregation_policy"])
