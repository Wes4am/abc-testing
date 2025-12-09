# backend/aggregator.py

from typing import List
from .schemas import VariantResult, BatchResult


def aggregate_variations(raw_responses: List[str]) -> BatchResult:
    """
    Aggregates raw JSON responses from Groq into structured VariantResult objects.

    Args:
        raw_responses: List of raw strings returned by Groq (JSON or plain text fallback)

    Returns:
        BatchResult object with list of VariantResult
    """

    results = []

    for idx, raw in enumerate(raw_responses, start=1):
        variant_text = raw

        # Attempt to parse JSON, fallback to raw text
        try:
            import json
            data = json.loads(raw)
            if isinstance(data, dict) and "variant_message" in data:
                variant_text = data["variant_message"]
        except Exception:
            pass  # keep raw text

        results.append(VariantResult(index=idx, variant_message=variant_text))

    return BatchResult(results=results)


if __name__ == '__main__':
    # simple test
    sample_raw = ['{"variant_message": "Hello there!"}', 'Fallback text']
    aggregated = aggregate_variations(sample_raw)
    print(aggregated.json(indent=2))
