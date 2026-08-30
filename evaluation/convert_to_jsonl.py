import json
import re
from pathlib import Path


INPUT_PATH = Path("data/dataset/dataset_raw.json")
OUTPUT_PATH = Path("data/dataset/dataset.jsonl")


def fix_multiline_strings(text):
    """Escape literal newlines inside JSON strings."""

    result = []

    inside_string = False
    escaped = False

    for char in text:

        if escaped:
            result.append(char)
            escaped = False
            continue

        if char == "\\" and inside_string:
            result.append(char)
            escaped = True
            continue

        if char == '"':
            inside_string = not inside_string
            result.append(char)
            continue

        if char == "\n" and inside_string:
            result.append("\\n")
        elif char == "\r" and inside_string:
            continue
        else:
            result.append(char)

    return "".join(result)


def remove_trailing_commas(text):
    """
    Remove commas immediately before } or ].
    Example:
        "correct": "text",
    }
    becomes:
        "correct": "text"
    }
    """

    return re.sub(r",(\s*[}\]])", r"\1", text)


def extract_top_level_objects(text):
    """Extract top-level JSON objects."""

    objects = []

    depth = 0
    inside_string = False
    escaped = False
    start = None

    for i, char in enumerate(text):

        if escaped:
            escaped = False
            continue

        if char == "\\" and inside_string:
            escaped = True
            continue

        if char == '"':
            inside_string = not inside_string
            continue

        if inside_string:
            continue

        if char == "{":

            if depth == 0:
                start = i

            depth += 1

        elif char == "}":

            depth -= 1

            if depth == 0 and start is not None:
                objects.append(text[start:i + 1])
                start = None

    return objects


def main():

    print("Reading dataset...")

    text = INPUT_PATH.read_text(encoding="utf-8")

    print("Fixing multiline strings...")
    text = fix_multiline_strings(text)

    print("Removing trailing commas...")
    text = remove_trailing_commas(text)

    print("Extracting records...")
    objects = extract_top_level_objects(text)

    print(f"Found {len(objects)} records.")

    records = []

    for i, obj in enumerate(objects, start=1):

        try:
            record = json.loads(obj)

        except json.JSONDecodeError as e:

            print(f"\nERROR in record {i}")
            print(e)

            print("\nProblematic section:")
            print(obj[-1500:])

            raise

        if not isinstance(record, dict):
            raise ValueError(
                f"Record {i} is not a dictionary."
            )

        records.append(record)

    print("Writing JSONL...")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:

        for record in records:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )

    print()
    print(f"Successfully converted {len(records)} records.")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()