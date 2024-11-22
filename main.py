import argparse
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
            page: pymupdf.Page = doc[page_num]

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


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="PDF to JSON Transformer")
    parser.add_argument("--input", help="Path to the input PDF file", type=str)
    parser.add_argument("--output", help="Path to save the output JSON file", type=str)
    args = parser.parse_args()

    # Determine execution mode (CLI or GUI)
    input_file = args.input
    output_file = args.output

    # GUI fallback logic
    if not input_file or not output_file:
        root = tk.Tk()
        root.withdraw()

    # Prompt for an input file if not provided
    if not input_file:
        input_file = askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not input_file:
            print("No PDF file selected.")
            return

    # Process the PDF file
    print(f"Processing PDF: {input_file}")
    text = extract_text_from_pdf(input_file)
    if text is None:
        print("Failed to extract text from PDF.")
        return

    # Prompt for an output file if not provided
    if not output_file:
        output_file = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not output_file:
            print("No file selected for saving output. Defaulting to './output.json'...")
            output_file = "output.json"

    # Save the processed data to JSON
    print(f"Saving JSON to: {output_file}")
    save_to_json(text, output_file)
    print("Processing complete!")


if __name__ == "__main__":
    main()
