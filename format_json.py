def sanitize_text(text: str) -> str:
    import re

    field_value: str = text.split(":")[-1].strip()
    return re.sub(pattern=r'\s+', repl=' ', string=field_value)

def sanitize_amount(amount: str) -> float:
    return float(amount.split()[-1].replace(",", "").replace("$", "").strip())


def format_json(data: dict) -> dict:
    # Extract GCPF/FPSC number from the details section
    details_text = data["details"]["text"]
    gcpf_number = None
    lines = details_text.split("\n")
    for line in lines:
        if "GCPF / FPSC" in line:
            gcpf_number = int(line.split()[-1].strip())

    # Extract recipient name, vendor number, program, and agreement
    recipient_name = None
    vendor_number = None
    program = None
    agreement = None
    for row in data["tables"][0]:
        if "Recipient Name" in row.get("Column_0", ""):
            recipient_name = sanitize_text(row.get("Column_0", ""))
            vendor_number = int(row.get("Column_1", "").split(":")[-1].strip())
            program = sanitize_text(row.get("Column_2", ""))
            agreement = sanitize_text(row.get("Column_3", ""))
            break

    # Extract grant contribution details from the table
    fiscal_years_data = {}  # Dictionary to group data by fiscal year
    total_payment_issued = 0.0  # Initialize total payment issued

    for page in data['tables']:
        for row in page:
            fiscal_year = row.get("Column_0", "").strip()

            # Check if the row contains fiscal year data
            if fiscal_year and "Funds Commitment Number" not in fiscal_year:
                try:
                    # Ensure the fiscal year is in the correct format (e.g., "2023-2024")
                    if "-" in fiscal_year and len(fiscal_year) == 9:
                        entry = {
                            "funds_commitment_number": int(row.get("Column_1", "").strip()),
                            "fund_centre": int(row.get("Column_2", "").strip()),
                            "authority_code": row.get("Column_3", "").strip(),
                            "gl_account": int(row.get("Column_4", "").strip()),
                            "internal_order": int(row.get("Column_5", "").strip()),
                            "description": sanitize_text(row.get("Column_6", "")),
                            "amount": sanitize_amount(row.get("Column_7", ""))
                        }

                        # Add the entry to the fiscal year's list
                        if fiscal_year not in fiscal_years_data:
                            fiscal_years_data[fiscal_year] = []
                        fiscal_years_data[fiscal_year].append(entry)
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}. Error: {e}")

            # Check if the row contains the total payment issued
            if "Total Payment Issued" in row.get("Column_0", ""):
                try:
                    total_payment_issued = sanitize_amount(row.get("Column_1", ""))
                except (ValueError, IndexError) as e:
                    print(f"Error processing total payment issued: {row}. Error: {e}")

    # Convert fiscal years data into a list format for JSON output
    grant_contribution_details = [
        {"fiscal_year": fiscal_year, "grant_data": entries}
        for fiscal_year, entries in fiscal_years_data.items()
    ]

    # Organize data into the required structure
    final_data = {
        "gcpf_number": gcpf_number,
        "recipient_name": recipient_name,
        "vendor_number": vendor_number,
        "program": program,
        "agreement": agreement,
        "grant_contribution_details": grant_contribution_details,
        "total_payment_issued": total_payment_issued,
    }

    return final_data
