import json
from pathlib import Path

from jiwer import cer, wer


DATASET_PATH = Path("data/dataset/dataset.jsonl")
PREDICTIONS_DIR = Path("data/baseline")


def load_dataset(path):
    examples = []

    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                examples.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse line {line_number}: {e}")

    return examples


def main():
    examples = load_dataset(DATASET_PATH)

    print(f"Loaded {len(examples)} examples.")

    total_cer = 0.0
    total_wer = 0.0
    valid_examples = 0

    for example in examples:
        image_path = Path(example["image_path"])
        corrected_text = example.get("corrected_text", "")

        document_name = image_path.parent.parent.name
        page_name = image_path.stem

        prediction_file = (
            PREDICTIONS_DIR / f"{document_name}_{page_name}.txt"
        )

        if not prediction_file.exists():
            print(f"Warning: Missing prediction: {prediction_file}")
            continue

        prediction_text = prediction_file.read_text(
            encoding="utf-8"
        )

        if not prediction_text.strip() and not corrected_text.strip():
            continue

        example_cer = cer(corrected_text, prediction_text)
        example_wer = wer(corrected_text, prediction_text)

        total_cer += example_cer
        total_wer += example_wer
        valid_examples += 1

        print(
            f"{document_name}/{page_name}: "
            f"CER={example_cer:.4f}, "
            f"WER={example_wer:.4f}"
        )

    if valid_examples == 0:
        raise ValueError("No valid examples found")

    average_cer = total_cer / valid_examples
    average_wer = total_wer / valid_examples

    print("\nZero-Shot Qwen Results")
    print(f"Valid examples: {valid_examples}")
    print(f"Average CER: {average_cer:.4f} ({average_cer * 100:.2f}%)")
    print(f"Average WER: {average_wer:.4f} ({average_wer * 100:.2f}%)")


if __name__ == "__main__":
    main()