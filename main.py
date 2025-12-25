from __future__ import annotations

import os

from orchestrator import ContentOrchestrator


def get_input_dataset():
    # The ONLY input dataset (no external facts)
    return {
        "Product Name": "GlowBoost Vitamin C Serum",
        "Concentration": "10% Vitamin C",
        "Skin Type": "Oily, Combination",
        "Key Ingredients": "Vitamin C, Hyaluronic Acid",
        "Benefits": "Brightening, Fades dark spots",
        "How to Use": "Apply 2–3 drops in the morning before sunscreen",
        "Side Effects": "Mild tingling for sensitive skin",
        "Price": "₹699",
    }


def main() -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")

    orchestrator = ContentOrchestrator()
    artifacts = orchestrator.run_pipeline(get_input_dataset(), output_dir=output_dir)

    written = artifacts.get("written_files", {}).get("written_files", {})
    print("Generated files:")
    for key, path in written.items():
        print(f"- {key}: {path}")

    # Also confirm question generation requirement
    q_total = artifacts.get("questions", {}).get("total_questions")
    print(f"Total questions generated: {q_total}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
