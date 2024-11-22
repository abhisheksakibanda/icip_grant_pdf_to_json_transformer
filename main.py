import json
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Optional

import camelot
import pymupdf
from dotenv import load_dotenv

from cleanup import json_cleanup

# Load ENV vars
load_dotenv()


def save_to_json(data: str, save_path: str = 'output.json') -> None:
    try:
        data_dict = json.loads(data)
        cleaned_json = json_cleanup(data_dict)

        with open(save_path, 'w', encoding='utf-8') as json_file:
            json.dump(cleaned_json, json_file, indent=4, ensure_ascii=False)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error processing JSON data: {e}")


def extract_text_from_pdf(path: str) -> Optional[str]:
    try:
        # Open the PDF file
        doc = pymupdf.open(path)

        # Initialize a dictionary to store extracted data
        result = {"text": "", "tables": []}

        # Iterate through all pages in the PDF
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract the plain text from the page
            page_text = page.get_text("text")
            result["text"] += page_text.strip() + "\n\n"

        # Extract tables using Camelot
        tables = camelot.read_pdf(path, pages="all", flavor="lattice")
        for table in tables:
            result["tables"].append(table.df.to_dict(orient="records"))

        # Close the document
        doc.close()

        # Convert the result to a JSON string and return
        return json.dumps(result, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        print("No PDF file selected.")
        return

    text = extract_text_from_pdf(pdf_path)
    if text is None:
        print("Failed to extract text from PDF.")
        return

    json_path = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if json_path:
        save_to_json(text, json_path)
    else:
        print("No file selected, saving to default path (./output.json)...")
        save_to_json(text)


if __name__ == "__main__":
    main()
