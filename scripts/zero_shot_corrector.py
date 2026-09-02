from pathlib import Path
from mlx_lm import load, generate


MODEL = "mlx-community/Qwen3-4B-Instruct-2507-4bit"

OCR_DIR = Path("data/ocr")
OUTPUT_DIR = Path("data/baseline")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print(f"Loading model: {MODEL}")

    model, tokenizer = load(MODEL)

    ocr_files = sorted(OCR_DIR.rglob("*.txt"))

    print(f"Found {len(ocr_files)} OCR files.")

    for i, ocr_file in enumerate(ocr_files, start=1):

        print(f"\n[{i}/{len(ocr_files)}] Processing: {ocr_file}")

        ocr_text = ocr_file.read_text(encoding="utf-8")

        prompt = f"""
You are an Arabic OCR post-correction system.

Correct the OCR errors in the Arabic text below.

Rules:
- Preserve the original meaning.
- Correct only errors supported by the text.
- Do not add explanations.
- Do not summarize.
- Do not rewrite or stylistically improve the text.
- Preserve punctuation and formatting when possible.
- Preserve diacritics when they are present.
- Return only the corrected Arabic text.

OCR text:
{ocr_text}
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True
        )

        response = generate(
            model,
            tokenizer,
            prompt=formatted_prompt,
            max_tokens=4096,
            verbose=False,
        )

        #Keep the same filename as the OCR input
        output_file = OUTPUT_DIR / f"{ocr_file.parent.name}_{ocr_file.name}"

        output_file.write_text(
            response.strip(),
            encoding="utf-8"
        )

        print(f"Saved: {output_file}")

    print("\nDone!")


if __name__ == "__main__":
    main()