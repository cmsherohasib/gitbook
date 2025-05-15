import os
from typing import Any

import uvicorn
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

PENDING_REQUESTS_FILE = "pending_requests.txt"


class PendingRequest(BaseModel):
    candidate_image_path: str
    reference_image_path: str


class SemanticIntegrityResult(BaseModel):
    candidate_image_path: str
    reference_image_path: str
    overall_prediction: bool
    tool_details: dict


def read_requests_from_file() -> list[tuple[str, str, str]]:
    """Reads lines of the form:
       candidate_image_path, reference_image_path, status

    Returns:
        list[tuple[str, str, str]]: a list of tuples:
            (candidate_image_path, reference_image_path, status)
    """
    if not os.path.exists(PENDING_REQUESTS_FILE):
        return []

    records = []
    with open(PENDING_REQUESTS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 3:
            candidate_img, reference_img, status = parts
            records.append((candidate_img, reference_img, status))
    return records


def write_requests_to_file(records: list[tuple[str, str, str]]) -> None:
    """Overwrites the file with records of the form:
       candidate_image_path, reference_image_path, status

    Args:
        records (list[tuple[str, str, str]]): a list of tuples:
            (candidate_image_path, reference_image_path, status)
    """
    with open(PENDING_REQUESTS_FILE, "w") as f:
        for candidate_img, reference_img, status in records:
            f.write(f"{candidate_img}, {reference_img}, {status}\n")


@app.get("/requests_pending_semantic_integrity", response_model=list[PendingRequest])
def get_requests_pending_semantic_integrity() -> list[PendingRequest]:
    """Get pending requests.

    Returns:
        list[PendingRequest]: the set of requests that are still in 'pending' state.
    """
    records = read_requests_from_file()
    pending = [(c, r) for (c, r, s) in records if s.lower() == "pending"]
    # Convert to Pydantic model
    return [PendingRequest(candidate_image_path=c, reference_image_path=r) for (c, r) in pending]


@app.post("/semantic_integrity_results")
def post_semantic_integrity_results(result: SemanticIntegrityResult) -> dict[str, Any]:
    """Receives the evaluation result for a (candidate_image_path, reference_image_path) pair,
    then marks that entry as 'processed' in the file.

    Args:
        result (SemanticIntegrityResult): Results of Semantic Integrity.

    Raises:
        HTTPException: if No pending entry found.

    Returns:
        dict[str, Any]: Message and results after posting results.
    """
    records = read_requests_from_file()
    found = False

    for i, (cand, ref, status) in enumerate(records):
        if (
            cand == result.candidate_image_path
            and ref == result.reference_image_path
            and status == "pending"
        ):
            # Mark it processed
            records[i] = (cand, ref, "processed")
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=404,
            detail=(
                "No pending entry found matching "
                f"candidate='{result.candidate_image_path}', "
                f"reference='{result.reference_image_path}'"
            ),
        )

    # Write updated entries back
    write_requests_to_file(records)

    return {
        "message": (
            "Semantic integrity result received and marked as processed "
            f"for candidate='{result.candidate_image_path}' "
            f"and reference='{result.reference_image_path}'."
        ),
        "result": {
            "overall_prediction": result.overall_prediction,
            "tool_details": result.tool_details,
        },
    }


@app.post("/requests_pending_semantic_integrity")
def add_file_to_pending(
    candidate_image_path: str = Body(...),
    reference_image_path: str = Body(...),
) -> dict[str, str]:
    """Add a new pair of (candidate_image_path, reference_image_path) to pending if not present.

    Args:
        candidate_image_path (str, optional): Candidate image path. Defaults to Body(...).
        reference_image_path (str, optional): Reference image path. Defaults to Body(...).

    Returns:
        dict[str, str]: Message showing successfull request.
    """
    candidate_image_path = candidate_image_path.strip()
    reference_image_path = reference_image_path.strip()

    records = read_requests_from_file()

    # Check if already present in any form
    for cand, ref, status in records:
        if cand == candidate_image_path and ref == reference_image_path:
            return {"message": f"This pair already exists with state '{status}'."}

    records.append((candidate_image_path, reference_image_path, "pending"))
    write_requests_to_file(records)
    return {
        "message": (
            f"Added pair candidate='{candidate_image_path}' & reference='{reference_image_path}' "
            "as pending."
        )
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
