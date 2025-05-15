import time
from dataclasses import dataclass
from typing import Any

import requests

SERVER_URL = "http://localhost:8000"


@dataclass
class SemanticIntegrityTool:
    """A tool for evaluating the integrity of images."""


@dataclass
class SemanticIntegrityChecker:
    """Evaluate images using multiple semantic integrity tools."""

    tools: list[SemanticIntegrityTool]
    aggregation_policy: str = "majority"

    def evaluate(
        self, reference_image_path: str, candidate_image_path: str
    ) -> tuple[bool, dict[str, dict[str, Any]]]:
        """Evaluate Semantic Integrity.

        Args:
            reference_image_path (str): Reference image path
            candidate_image_path (str): Candidate image path.

        Returns:
            tuple[bool, dict[str, dict[str, Any]]]: Tuple containing the overall prediction
                and Tool details.
        """
        print(
            """Evaluating integrity with tools...
Captioning reference_image_path...
Captioning candidate_image_path...
Comparing captions...
Compute embeddings for both captions...
Compute cosine similarity...
ImageCaptioningTool:  50%
ObjectDetectionTool: 100%
Aggregating tool responses..."""
        )
        # Return a mock decision
        return True, {
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
        }


def retrieve_pending_pairs() -> list[tuple[str, str, str]]:
    """Fetch the list of pending requests (candidate & reference).

    Returns:
        list[tuple[str, str, str]]: a list of tuples:
            (candidate_image_path, reference_image_path, status)
    """
    response = requests.get(f"{SERVER_URL}/requests_pending_semantic_integrity")
    response.raise_for_status()
    return response.json()


def post_semantic_integrity_results(
    candidate_img: str,
    reference_img: str,
    overall_pred: bool,
    tool_details: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Post evaluation results back to the server to mark them processed.

    Args:
        candidate_img (str): Candidate image path.
        reference_img (str): Reference image path
        overall_pred (bool): Overall prediction.
        tool_details (dict[str, dict[str, Any]]): Detailed results from each tool mentioned in
            semantic integtity.

    Returns:
        dict[str, Any]: Message and results after posting results.
    """
    endpoint = f"{SERVER_URL}/semantic_integrity_results"
    data = {
        "candidate_image_path": candidate_img,
        "reference_image_path": reference_img,
        "overall_prediction": overall_pred,
        "tool_details": tool_details,
    }
    response = requests.post(endpoint, json=data)
    response.raise_for_status()
    return response.json()


def main_loop(interval_seconds: int = 300) -> None:
    """Main loop to keep checking for pending requests and post the results of semantic integrity.

    Args:
        interval_seconds (int, optional): Interval seconds. Defaults to 300.
    """
    checker = SemanticIntegrityChecker(tools=[])
    while True:
        print("Checking for pending image pairs...")
        try:
            pending_list = retrieve_pending_pairs()
            print(f"Found {len(pending_list)} pending pairs.")
            for item in pending_list:
                candidate_img = item["candidate_image_path"]
                reference_img = item["reference_image_path"]
                print(f"Evaluating: candidate={candidate_img}, reference={reference_img}")

                # Evaluate the images
                overall, tool_details = checker.evaluate(reference_img, candidate_img)

                # Post the results
                print(f"Posting results for candidate={candidate_img}, reference={reference_img}")
                resp = post_semantic_integrity_results(
                    candidate_img, reference_img, overall, tool_details
                )
                print("Server response:", resp)
        except Exception as ex:
            print("Error during processing:", ex)

        print(f"Sleeping for {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main_loop(interval_seconds=60)
