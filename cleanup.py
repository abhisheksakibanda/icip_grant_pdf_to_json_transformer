from format_json import format_json


def json_cleanup(data: dict) -> dict:
    # Extract and clean text
    cleaned_text = data["text"].strip()

    # Clean and structure tables
    cleaned_tables = []
    for table in data["tables"]:
        structured_table = []
        for row in table:
            # Remove empty rows
            if not any(row.values()):
                continue

            # Combine columns into key-value pairs where possible
            counter: int = 0
            structured_row: dict[str, str] = {}

            for value in row.values():
                if value.strip():
                    structured_row[f"Column_{counter}"] = value.strip()
                    counter += 1
            # structured_row = {f"Column_{i}": value.strip() for i, value in enumerate(row.values()) if value.strip()}
            structured_table.append(structured_row)

        if structured_table:
            cleaned_tables.append(structured_table)

    # Organize data into sections
    cleaned_data = {
        "details": {
            "text": cleaned_text.split("B. Signatures")[0].strip()
        },
        "signatures": {
            "text": cleaned_text.split("B. Signatures")[1].strip() if "B. Signatures" in cleaned_text else ""
        },
        "tables": cleaned_tables,
    }

    return format_json(cleaned_data)
