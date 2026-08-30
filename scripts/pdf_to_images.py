from pathlib import Path
import pymupdf # PyMuPDF

RAW_DIR = Path("data/raw")

#Pages to extract for each document
pages_to_extract = {
    1: [88, 111],
    2: [57, 59],
    3: [82, 88],
    4: [156, 180],
    5: [54, 68],
}

for i, pdf_path in enumerate(sorted(RAW_DIR.rglob("*.pdf")), start=1):

    if i not in pages_to_extract:
        continue

    document_dir = pdf_path.parent
    output_dir = document_dir / "images"
    output_dir.mkdir(exist_ok=True)

    doc = pymupdf.open(pdf_path)

    print(f"\nProcessing: {pdf_path}")
    print(f"Pages: {len(doc)}")

    zoom = 300 / 72
    matrix = pymupdf.Matrix(zoom, zoom)

    for page_number in pages_to_extract[i]:

        #Convert human page number to Python index
        page_index = page_number - 1

        if page_index < 0 or page_index >= len(doc):
            print(f"WARNING: Page {page_number} does not exist.")
            continue

        page = doc[page_index]

        pix = page.get_pixmap(
            matrix=matrix,
            colorspace=pymupdf.csRGB,
            alpha=False
        )

        output_path = output_dir / f"page_{page_number:04d}.png"
        pix.save(output_path)

        print(f"Saved: {output_path}")

    doc.close()