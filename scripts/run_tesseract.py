from pathlib import Path
import subprocess

RAW_DIR = Path("data/raw")
OCR_DIR = Path("data/ocr")

OCR_DIR.mkdir(parents=True, exist_ok=True)

for image_path in sorted(RAW_DIR.rglob("*.png")):

    #doc_001, doc_002, etc.
    document_dir = image_path.parent.parent
    document_id = document_dir.name

    output_dir = OCR_DIR / document_id
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{image_path.stem}.txt"

    print(f"OCR: {image_path}")

    subprocess.run(
        [
            "tesseract",
            str(image_path),
            str(output_path.with_suffix("")),
            "-l",
            "ara",
            "--psm",
            "3",
        ],
        check=True,
    )

print("OCR completed.")