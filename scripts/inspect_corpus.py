from pathlib import Path
from pypdf import PdfReader

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def list_files() -> list[Path]:
    """Return every file in data/raw/, sorted by name."""
    return sorted(p for p in RAW_DIR.iterdir() if p.is_file())

def main() -> None:
    files = list_files()
    if not files:
        print("No files found in {RAW_DIR}}")
        return

    print (f"Found {len(files)} files in {RAW_DIR}:")

    suspects = []

    for file in files:
        size_in_kb = file.stat().st_size / 1024

        if file.suffix.lower() == ".pdf":
            page_count, char_count = check_pdf_text(file)
            chars_per_page = char_count / page_count if page_count > 0 else 0
            flag = " <-- LOW TEXT, check this one" if chars_per_page < 100 else ""
            print(f"  {file.name:<55} {size_in_kb:>8.1f} KB   {page_count:>3} pages   {char_count:>7} chars{flag}")
            if flag:
                suspects.append(file.name)
        else:
            print(f"  {file.name:<35} ({size_in_kb:.2f} KB) - {page_count} pages, {char_count} characters")

    if suspects:
        print(f"\n{len(suspects)} file(s) may be scanned/low-text: {', '.join(suspects)}")
    else:
        print("\nAll PDFs have extractable text. Good to proceed.")

def check_pdf_text(path: Path) -> tuple[int, int]:
    """Return (page count, character count) in a pdf."""
    try:
        reader = PdfReader(path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return len(reader.pages), len(text)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return 0, 0

if __name__ == "__main__":
    main()